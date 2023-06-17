import great_expectations
from great_expectations.core import ExpectationConfiguration

from ....systems.connectors import Connector
from ....systems.models import DbTable
from ..exceptions import GXException
from . import CheckExecutor, ExpectationResult


class ExpectationExecutor(CheckExecutor):
    DATASOURCE_NAME: str = "inspector_sqla_datasource"
    CONNECTOR_NAME: str = "inspector_sqla_connector"
    EXECUTION_ENGINE_NAME: str = "inspector_sqla_execution_engine"

    def execute(self):
        context = great_expectations.get_context()

        expectation_kwargs = {}
        if not self.datacheck.left_expectation.table_level:
            expectation_kwargs["column"] = self.datacheck.left_column
        expectation_config = ExpectationConfiguration(
            expectation_type=self.datacheck.left_expectation.name, kwargs=expectation_kwargs
        )

        context.add_expectation_suite(expectation_suite_name=self.datacheck.code, expectations=[expectation_config])

        connector = Connector.get_connector_for_instance(self.instance)

        table = DbTable.objects.get(instance_id=self.instance.id, dataset_id=self.datacheck.left_dataset_id)
        datasource = context.sources.add_sql(name=table.name, connection_string=connector.sqla_connection_string)

        table_asset = datasource.add_table_asset(name=table.name, table_name=table.name)

        batch_request = table_asset.build_batch_request()

        checkpoint = context.add_checkpoint(self.datacheck.code)

        result = checkpoint.run(expectation_suite_name=self.datacheck.code, batch_request=batch_request)

        result_detail = list(result["run_results"].items())[0][1]["validation_result"]["results"][0]

        if result_detail["exception_info"]["raised_exception"]:
            raise GXException(result_detail["exception_info"]["exception_message"])

        return ExpectationResult(result=result["success"], object_value=result_detail["result"])
