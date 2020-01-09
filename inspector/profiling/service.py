import logging
import os
from abc import ABCMeta
from datetime import datetime as dt
from tempfile import gettempdir
from typing import Optional

from django.core.files import File
from pytz import utc

from .models import TableProfile
from ..base.constants import STATUSES
from ..base.mixins import ExceptionCollectorMixin
from ..systems.connectors import Connector, get_connector_for_instance
from ..systems.models import Instance

logger = logging.getLogger(__name__)


class ProfilerService(ExceptionCollectorMixin, metaclass=ABCMeta):
    def __init__(self, profile: TableProfile, mode: str):
        super().__init__()
        self.profile: TableProfile = profile
        self.mode: str = mode

        instance = Instance.objects.get(
            system=profile.dbtable.system, environment=profile.dbtable.environment
        )
        self.connector: Connector = get_connector_for_instance(instance)
        self.report_file_name: Optional[str] = None
        self.report_file_path: Optional[str] = None

    def profile_table(self):
        raise NotImplementedError

    def run_profiling(self):
        if self.status:
            try:
                self.profile_table()
            except Exception as exc:
                self.add_exception(exc)

    def start_profiling(self):
        self.profile.start_time = dt.now(tz=utc)
        self.profile.status = STATUSES.RUNNING
        self.profile.save()
        self.report_file_name = (
            "__".join(
                [
                    self.profile.dbtable.system.name,
                    self.profile.dbtable.environment.name,
                    self.profile.dbtable.fullname,
                    self.profile.start_time.strftime("%Y%m%d_%H%M%S"),
                ]
            )
            + ".html"
        )
        self.report_file_path = os.path.join(gettempdir(), self.report_file_name)

    def save_report(self):
        if self.status:
            try:
                with open(self.report_file_path, "rb") as report_file:
                    self.profile.result.save(
                        name=self.report_file_name, content=File(report_file)
                    )
            except Exception as exc:
                self.add_exception(exc)

    def save_profile(self):
        if self.status:
            self.profile.end_time = dt.now(tz=utc)
            self.profile.status = STATUSES.FINISHED
            self.profile.dbtable.rows = self.profile.rows
            self.profile.dbtable.last_profiling_at = dt.now(tz=utc)
            self.profile.dbtable.save()
        else:
            self.profile.error_message = self.errors_text()
            self.profile.status = STATUSES.ERROR
        self.profile.save()


class PandasProfilerService(ProfilerService):
    def profile_table(self):
        from pandas import read_sql_table
        from pandas_profiling import ProfileReport

        self.connector.get_engine()
        self.connector.test_connection()
        logging.info("Loading table into DataFrame")
        df = read_sql_table(
            table_name=self.profile.dbtable.name,
            con=self.connector.engine,
            schema=self.profile.dbtable.schema,
        )
        self.profile.rows = len(df.index)
        logging.info("Generating Pandas Profiling report")
        profile_report = ProfileReport(
            df, title=self.report_file_name, minimal=self.mode == "pandas_minimal"
        )
        logging.info("Saving profiling report: %s", self.report_file_path)
        profile_report.to_file(self.report_file_path)
