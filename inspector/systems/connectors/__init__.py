import dataclasses
import typing
from abc import ABCMeta, abstractmethod
from importlib import import_module

from ..models import Instance

if typing.TYPE_CHECKING:
    from pandas import DataFrame


@dataclasses.dataclass
class Dataset:
    name: str
    schema: str | None = None
    db: str | None = None

    @property
    def fullname(self):
        name = []
        if self.db:
            name.append(self.db)
        if self.schema:
            name.append(self.schema)
        name.append(self.name)

        return ".".join(name)


class Connector(metaclass=ABCMeta):
    def __init__(self, instance: Instance):
        self.instance: Instance = instance

    @property
    def sqla_connection_string(self) -> str:
        """Return the connection string for the connector"""
        return ""

    def test_connection(self):
        pass

    @abstractmethod
    def get_datasets(self) -> dict[str, Dataset]:
        """Return a list of datasets"""

    @abstractmethod
    def table_df(self, table: str, schema: str = None) -> "DataFrame":
        """Return a pandas DataFrame for the given table"""
        pass

    @staticmethod
    def get_connector_for_instance(instance: Instance) -> "Connector":
        connector_module = import_module(f"inspector.systems.connectors.{instance.system.application}_connector")
        connector_class = getattr(connector_module, instance.system.application.capitalize() + "Connector")
        return connector_class(
            instance=instance,
        )
