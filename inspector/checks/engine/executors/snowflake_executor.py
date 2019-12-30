from .sql_executor import SQLExecutor
from ....systems.connectors.snowflake_connector import SnowflakeConnector


class SnowflakeExecutor(SQLExecutor, SnowflakeConnector):
    pass
