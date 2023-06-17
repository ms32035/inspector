import logging
import typing
from datetime import datetime as dt
from importlib import import_module

from django.core.files import File
from pytz import utc

from ..base.models import Statuses

if typing.TYPE_CHECKING:
    from .models import TableProfile
    from .profilers import Profiler

logger = logging.getLogger(__name__)


class ProfilerService:
    @staticmethod
    def get_profiler(profile: "TableProfile") -> "Profiler":
        executor_module = import_module(f"inspector.profiling.profilers.{profile.profiler}_profiler")
        profiler_class = getattr(executor_module, f"{profile.profiler.capitalize()}Profiler")

        return profiler_class(profile)

    @staticmethod
    def begin_profiling(profile: "TableProfile"):
        profile.start_time = dt.now(tz=utc)
        profile.status = Statuses.RUNNING
        profile.save()

    @staticmethod
    def profile_table(profile: "TableProfile", profiler: "Profiler"):
        profiler.set_report_file_name(
            "__".join(
                [
                    profile.dbtable.instance.system.name,
                    profile.dbtable.instance.environment.name,
                    profile.dbtable.fullname,
                    profile.start_time.strftime("%Y%m%d_%H%M%S"),
                ]
            )
        )
        result = profiler.profile_table()

        profile.rows = result.rows
        profile.end_time = dt.now(tz=utc)
        profile.status = Statuses.FINISHED
        profile.dbtable.rows = result.rows
        profile.variables = result.variables
        profile.dbtable.last_profiling_at = dt.now(tz=utc)
        profile.dbtable.save()
        profile.save()

    @staticmethod
    def save_report(profile: "TableProfile", profiler: "Profiler"):
        with open(profiler.report_file_path, "rb") as report_file:
            profile.result.save(name=profiler.report_file_name, content=File(report_file))

    @staticmethod
    def save_error(profile: "TableProfile", exc: Exception):
        profile.error_message = repr(exc)
        profile.status = Statuses.ERROR
        profile.save()
