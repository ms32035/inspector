from abc import ABCMeta
from typing import Tuple, Optional

from ..exceptions import CheckTypeNotSupported
from ....systems.constants import APPLICATIONS
from ....systems.models import Instance
from ....systems.connectors import Connector

EXECUTOR_SQL = {"module": "sql_executor", "class": "SQLExecutor"}

EXECUTOR_SNOWFLAKE = {"module": "snowflake_executor", "class": "SnowflakeExecutor"}

CONFIG = {
    APPLICATIONS.POSTGRES: EXECUTOR_SQL,
    APPLICATIONS.REDSHIFT: EXECUTOR_SQL,
    APPLICATIONS.MYSQL: EXECUTOR_SQL,
    APPLICATIONS.SNOWFLAKE: EXECUTOR_SNOWFLAKE,
}


class CheckExecutor(Connector, metaclass=ABCMeta):
    supported_check_types: Tuple = tuple()

    def __init__(self, instance: Optional[Instance], check_type):
        Connector.__init__(self, instance)
        self.check_type = check_type
        if check_type not in self.supported_check_types:
            raise CheckTypeNotSupported

    def execute(self, check_logic):
        pass
