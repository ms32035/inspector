import dataclasses
import logging
import os
from abc import ABCMeta, abstractmethod
from datetime import datetime as dt
from tempfile import gettempdir

from ...systems.connectors import Connector
from ..models import TableProfile

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class ProfilingResult:
    rows: int
    variables: int


class Profiler(metaclass=ABCMeta):
    extension = "html"
    connector: Connector

    def __init__(self, profile: TableProfile):
        self.profile: TableProfile = profile
        self.connector = Connector.get_connector_for_instance(profile.dbtable.instance)
        self.start_time: dt | None = None
        self.report_file_path: str | None = None
        self.report_file_name: str | None = None

    @abstractmethod
    def profile_table(self) -> ProfilingResult:
        """Profile table"""

    def set_report_file_name(self, base_name: str):
        self.report_file_name = base_name + "." + self.extension
        self.report_file_path = os.path.join(gettempdir(), self.report_file_name)
