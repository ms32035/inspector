import typing

from pandas import DataFrame, read_sql_table
from sqlalchemy.engine import create_engine, reflection

if typing.TYPE_CHECKING:
    from sqlalchemy.engine import Engine

from . import Connector, Dataset


class SQLConnector(Connector):
    sqla_connection_string_template: str
    jdbc_connection_string_template: str
    jar_package: str
    jdbc_driver_class: str
    default_port: int

    def __init__(self, instance):
        super().__init__(instance)
        self.engine: "Engine" = self.get_engine()

    def get_engine(self) -> "Engine":
        kwargs = self.instance.extra_json or {}
        self.engine = create_engine(self.sqla_connection_string, **kwargs)
        return self.engine

    @property
    def sqla_connection_string(self) -> str:
        return self.sqla_connection_string_template.format(
            login=self.instance.login,
            password=self.instance.password,
            host=self.instance.host,
            port=self.instance.port or self.default_port,
            db=self.instance.db,
        )

    @property
    def jdbc_connection_string(self) -> str:
        return self.jdbc_connection_string_template.format(
            host=self.instance.host,
            port=self.instance.port or self.default_port,
            db=self.instance.db,
        )

    def test_connection(self):
        connection = self.engine.connect()
        connection.close()

    def get_datasets(self) -> dict[str, Dataset]:
        tables = dict()
        insp = reflection.Inspector.from_engine(self.engine)
        schemas = insp.get_schema_names()
        for schema in schemas:
            schema_tabs = insp.get_table_names(schema=schema)
            for tab in schema_tabs:
                dts = Dataset(name=tab, schema=schema)
                tables[dts.fullname] = dts
        return tables

    def table_df(self, table: str, schema: str = None) -> DataFrame:
        return read_sql_table(con=self.engine, table_name=table, schema=schema)

    @property
    def jdbc_options(self) -> dict[str, str]:
        return {
            "driver": self.jdbc_driver_class,
            "user": self.instance.login,
            "password": self.instance.password,
        }
