from sqlalchemy import text

from .sql_executor import SQLExecutor


class SqlQueryExecutor(SQLExecutor):
    def get_query_text(self, check_logic: str):
        return text(check_logic)
