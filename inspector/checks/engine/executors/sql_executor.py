import typing
from abc import abstractmethod
from datetime import datetime

from ....systems.models import Instance
from ..exceptions import TooManyRows
from . import CheckExecutor, Result

if typing.TYPE_CHECKING:
    from ....checks.models import Datacheck

from ....systems.connectors.sql_connector import SQLConnector


class SQLExecutor(CheckExecutor):
    def __init__(self, datacheck: "Datacheck", side: str, instance: Instance | None):
        super().__init__(datacheck, side, instance)
        self.sql_connector: SQLConnector = SQLConnector.get_connector_for_instance(instance)

    def test_connection(self):
        connection = self.sql_connector.engine.connect()
        connection.close()

    @staticmethod
    @abstractmethod
    def get_query_text(check_logic: str):
        """Convert check logic to sql query text"""

    def execute(self):
        check_logic = getattr(self.datacheck, f"{self.side}_logic")
        self.sql_connector.get_engine()
        with self.sql_connector.engine.connect() as connection:
            res = connection.execute(self.get_query_text(check_logic))
            if res.rowcount > 1:
                raise TooManyRows
            row = res.fetchone()

        cols = len(row)
        if cols == 1:
            if isinstance(row[0], (int, float)):
                return Result("number", number_value=row[0])
            elif isinstance(row[0], str):
                return Result("string", string_value=row[0])
            elif isinstance(row[0], datetime):
                return Result("date", date_value=row[0].replace(tzinfo=None))

        raise TypeError("Invalid result type")
