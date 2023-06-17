import typing

from great_expectations.core.batch import BatchRequest
from great_expectations.data_context import EphemeralDataContext
from great_expectations.data_context.types.base import (
    AnonymizedUsageStatisticsConfig,
    DataContextConfig,
    InMemoryStoreBackendDefaults,
    ProgressBarsConfig,
)
from great_expectations.datasource import Datasource

if typing.TYPE_CHECKING:
    from ..systems.models import DbTable


class GxClient:
    DATASOURCE_NAME: str = "inspector_sqla_datasource"
    CONNECTOR_NAME: str = "inspector_sqla_connector"
    EXECUTION_ENGINE_NAME: str = "inspector_sqla_execution_engine"

    def __init__(self):
        self.context: EphemeralDataContext = EphemeralDataContext(
            project_config=DataContextConfig(
                store_backend_defaults=InMemoryStoreBackendDefaults(),
                anonymous_usage_statistics=AnonymizedUsageStatisticsConfig(enabled=False),
                progress_bars=ProgressBarsConfig(globally=False, profilers=False, metric_calculations=False),
            )
        )

    def add_datasource(self, table: "DbTable", connection_string: str):
        asset_dict = {"table_name": table.name}
        if table.schema:
            asset_dict["schema_name"] = table.schema

        datasource = Datasource(
            name=self.DATASOURCE_NAME,
            data_connectors={
                self.CONNECTOR_NAME: {
                    "class_name": "ConfiguredAssetSqlDataConnector",
                    "assets": {
                        table.fullname: asset_dict,
                    },
                }
            },
            execution_engine={
                "class_name": "SqlAlchemyExecutionEngine",
                "connection_string": connection_string,
            },
        )

        self.context.add_datasource(datasource=datasource)

    @staticmethod
    def batch_request(
        table: "DbTable", datasource_name: str = DATASOURCE_NAME, data_connector_name: str = CONNECTOR_NAME
    ) -> BatchRequest:
        return BatchRequest(
            datasource_name=datasource_name,
            data_connector_name=data_connector_name,
            data_asset_name=table.fullname,
        )

    def add_checkpoint(self, name: str):
        self.context.add_checkpoint(
            name=name,
            config_version=1.0,
            class_name="SimpleCheckpoint",
            run_name_template=f"{name}-%Y%m%d-%H%M%S",
            expectation_suite_name=name,
        )
