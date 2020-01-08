from . import CheckExecutor
from ...constants import CHECK_TYPES
from ....systems.connectors.sql_connector import SQLConnector
from ..exceptions import TooManyValues


class SQLExecutor(CheckExecutor, SQLConnector):
    supported_check_types = (CHECK_TYPES.SQL_QUERY, CHECK_TYPES.SQL_EXPRESSION)

    def execute(self, check_logic):
        connection = self.engine.connect()
        res = connection.execute(check_logic)
        if res.rowcount > 1:
            raise TooManyValues
        row = res.fetchone()
        if len(row) > 1:
            raise TooManyValues
        connection.close()
        return row[0]
