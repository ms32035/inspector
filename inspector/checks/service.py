import typing

from django.db import transaction
from taggit.models import Tag

from inspector.taskapp.tasks import execute_check

from ..systems.query import DbTableQuery, EnvironmentQuery, InstanceQuery
from .models import CheckRun, Datacheck
from .query import CheckRunQuery, DatacheckQuery

if typing.TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser


class CheckRunService:
    @staticmethod
    def create_check_run_api(check_code: str, environment: str, user: "AbstractBaseUser") -> "CheckRun":
        return CheckRunService.create_and_execute_checkrun(
            DatacheckQuery.get(code=check_code), EnvironmentQuery.get(name=environment).id, user
        )

    @staticmethod
    def create_check_run(check_id: int, environment_id: int, user: "AbstractBaseUser") -> "CheckRun":
        return CheckRunService.create_and_execute_checkrun(
            DatacheckQuery.get(id=check_id), environment_id=environment_id, user=user
        )

    @staticmethod
    def run_check_tag(tag: Tag, environment_id: int, user: "AbstractBaseUser") -> list["CheckRun"]:
        return [
            CheckRunService.create_and_execute_checkrun(chk, environment_id, user)
            for chk in Datacheck.objects.filter(tags__name__in=[tag.name]).order_by("-weight")
        ]

    @staticmethod
    def create_and_execute_checkrun(check: "Datacheck", environment_id: int, user: "AbstractBaseUser") -> "CheckRun":
        left_instance = (
            InstanceQuery.system_environment(check.left_system_id, environment_id) if check.left_system_id else None
        )
        right_instance = (
            InstanceQuery.system_environment(check.right_system_id, environment_id) if check.right_system_id else None
        )
        warning_instance = (
            InstanceQuery.system_environment(check.warning_system_id, environment_id)
            if check.warning_system_id
            else None
        )

        check_run = CheckRun(
            datacheck=check,
            environment_id=environment_id,
            user=user,
            left_instance=left_instance,
            left_table=(
                DbTableQuery.dataset_environment(check.left_dataset_id, environment_id)
                if check.left_dataset_id
                else None
            ),
            left_dataset_id=check.left_dataset_id,
            right_instance=right_instance,
            warning_instance=warning_instance,
            left_expectation_id=check.left_expectation_id,
            relation=check.relation,
            warning_relation=check.warning_relation,
            left_column=check.left_column,
        )
        with transaction.atomic():
            check_run.save()
            transaction.on_commit(lambda: execute_check.delay(check_run.id))

        return check_run

    @staticmethod
    def checkrun_rerun(checkrun_id: int, user: "AbstractBaseUser") -> "CheckRun":
        checkrun = CheckRunQuery.datacheck_environment(checkrun_id)
        return CheckRunService.create_and_execute_checkrun(
            check=checkrun.datacheck, environment_id=checkrun.environment_id, user=user
        )
