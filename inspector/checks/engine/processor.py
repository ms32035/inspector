import logging
import operator
from datetime import datetime as dt
from importlib import import_module

from pytz import utc

from ...base.models import Statuses
from ..models import CheckRun, Datacheck
from .executors import CheckExecutor, ExpectationResult, Result

logger = logging.getLogger(__name__)


class CheckProcessor:
    SQL_TYPES = ("sql_query", "sql_expression")
    OPERATORS = {
        "eq": operator.eq,
        "ne": operator.ne,
        "gt": operator.gt,
        "lt": operator.lt,
        "ge": operator.ge,
        "le": operator.le,
    }

    def __init__(self, checkrun_id: int):
        self.checkrun: CheckRun = CheckRun.objects.select_related("datacheck").get(id=checkrun_id)
        self.datacheck: Datacheck = self.checkrun.datacheck
        self.left_executor: CheckExecutor | None = None
        self.right_executor: CheckExecutor | None = None
        self.warning_executor: CheckExecutor | None = None

    def prepare_check(self) -> bool:
        try:
            self.left_executor = self.get_executor(side="left")

            if self.datacheck.right_type:
                self.right_executor = self.get_executor(side="right")

            if self.datacheck.supports_warning:
                self.warning_executor = self.get_executor(side="warning")

            logger.info("Starting check -  %s", self.datacheck.code)

            self.checkrun.status = Statuses.RUNNING
            self.checkrun.start_time = dt.now(utc)

        except Exception as exc:
            import traceback

            traceback.print_exc()
            self.checkrun.status = Statuses.ERROR
            self.checkrun.error_message = repr(exc)

        self.checkrun.save()

        return self.checkrun.status == Statuses.RUNNING

    def get_executor(self, side: str) -> CheckExecutor:
        check_type = getattr(self.datacheck, f"{side}_type")
        executor_module = import_module(f"inspector.checks.engine.executors.{check_type}_executor")
        class_name = "".join([x.capitalize() for x in check_type.split("_")])
        executor_class = getattr(executor_module, f"{class_name}Executor")

        return executor_class(
            datacheck=self.datacheck,
            side=side,
            instance=getattr(self.checkrun, f"{side}_instance"),
        )

    def execute_checks(self) -> bool:
        try:
            self.save_value(left_result := self.left_executor.execute(), side="left")

            if isinstance(left_result, ExpectationResult):
                self.save_outcome(
                    Statuses.FINISHED, CheckRun.Results.SUCCESS if left_result.result else CheckRun.Results.FAILED
                )
                return True

            self.save_value(right_result := self.right_executor.execute(), side="right")

            if self.compare(left_result, right_result, self.datacheck.relation):
                self.save_outcome(Statuses.FINISHED, CheckRun.Results.SUCCESS)
                return True

            if self.datacheck.supports_warning:
                warning_result = self.warning_executor.execute()
                self.save_value(warning_result, side="warning")

                warning_comparison_result = self.compare(left_result, warning_result, self.datacheck.warning_relation)
                if warning_comparison_result:
                    self.save_outcome(Statuses.FINISHED, CheckRun.Results.WARNING)
                    return True

            self.save_outcome(Statuses.FINISHED, CheckRun.Results.FAILED)

        except Exception as exc:
            self.checkrun.error_message = repr(exc)
            self.save_outcome(Statuses.ERROR)

        return False

    def save_outcome(self, status, result=None):
        self.checkrun.result = result
        self.checkrun.end_time = dt.now(utc)
        self.checkrun.status = status
        self.checkrun.save()

    def compare(self, first, second, relation: str) -> bool:
        return self.OPERATORS[relation](first, second)

    def save_value(self, result: Result | ExpectationResult, side: str):
        if isinstance(result, ExpectationResult):
            self.checkrun.left_value_type = "expectation"
            self.checkrun.left_object_value = result.object_value
        else:
            setattr(self.checkrun, f"{side}_{result.value_type}_value", result.value)
            setattr(self.checkrun, f"{side}_value_type", result.value_type)
