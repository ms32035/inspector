from . import CheckExecutor
from ..exceptions import TooManyRows
from ...constants import CHECK_TYPES
from ....systems.connectors.sql_connector import SQLConnector


class SQLExecutor(CheckExecutor, SQLConnector):
    supported_check_types = (CHECK_TYPES.SQL_QUERY, CHECK_TYPES.SQL_EXPRESSION)

    def execute(self, check_logic):
        connection = self.engine.connect()
        res = connection.execute(check_logic)
        if res.rowcount > 1:
            raise TooManyRows
        row = res.fetchone()
        val = str(row) if len(row) > 1 else row[0]

        connection.close()
        return val
