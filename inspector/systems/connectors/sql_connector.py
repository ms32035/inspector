from sqlalchemy.engine import create_engine

from . import Connector
from ..constants import APPLICATIONS

CONNECTION_STRINGS = {
    APPLICATIONS.POSTGRES: "postgres+psycopg2://{login}:{password}@{host}:{port}/{db}",
    APPLICATIONS.REDSHIFT: "redshift+psycopg2://{login}:{password}@{host}:{port}/{db}",
    APPLICATIONS.MYSQL: "mysql://{login}:{password}@{host}:{port}/{db}",
}


class SQLConnector(Connector):
    def get_engine(self) -> None:
        connection_string = CONNECTION_STRINGS[self.instance.system.application]
        kwargs = self.instance.extra_json or {}
        self.engine = create_engine(
            connection_string.format(
                login=self.instance.login,
                password=self.instance.password,
                host=self.instance.host,
                port=self.instance.port,
                db=self.instance.db,
            ),
            **kwargs
        )

    def test_connection(self):
        connection = self.engine.connect()
        connection.close()
