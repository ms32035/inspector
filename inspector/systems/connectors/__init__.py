from abc import ABCMeta
from importlib import import_module
from typing import Optional

from sqlalchemy.engine import Engine

from ..constants import APPLICATIONS
from ..models import Instance

CONNECTOR_SQL = {"module": "sql_connector", "class": "SQLConnector"}

CONNECTOR_SNOWFLAKE = {"module": "snowflake_connector", "class": "SnowflakeConnector"}

CONFIG = {
    APPLICATIONS.POSTGRES: CONNECTOR_SQL,
    APPLICATIONS.REDSHIFT: CONNECTOR_SQL,
    APPLICATIONS.MYSQL: CONNECTOR_SQL,
    APPLICATIONS.SNOWFLAKE: CONNECTOR_SNOWFLAKE,
}


class Connector(metaclass=ABCMeta):
    engine: Optional[Engine] = None

    def __init__(self, instance: Instance):
        self.instance: Instance = instance

    def get_engine(self):
        pass

    def test_connection(self):
        pass


def get_connector_for_instance(instance: Instance):
    config = CONFIG[instance.system.application]
    connector_module = import_module(f'inspector.systems.connectors.{config["module"]}')
    connector_class = getattr(connector_module, config["class"])
    return connector_class(instance=instance,)
