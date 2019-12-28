from json import loads

from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

from .sql_connector import SQLConnector


class SnowflakeConnector(SQLConnector):
    def get_engine(self):
        json_data = loads(self.instance.extra_json)
        self.engine = create_engine(
            URL(
                user=self.instance.login,
                password=self.instance.password,
                account=json_data["account"],
                region=json_data["region"],
                database=self.instance.db,
                warehouse=json_data["warehouse"],
                role=json_data["role"],
            )
        )
