from pandas import DataFrame
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

from .sql_connector import SQLConnector


class SnowflakeConnector(SQLConnector):
    def get_engine(self):
        json_data = self.instance.extra_json
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
        return self.engine

    def table_df(self, table: str, schema: str = None) -> DataFrame:
        cur = self.engine.raw_connection().cursor()
        sql = f"SELECT * FROM {schema}.{table}"
        cur.execute(sql)
        return cur.fetch_pandas_all()
