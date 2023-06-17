import typing

from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
from great_expectations.validator.metric_configuration import MetricConfiguration

from ...base.gx import GxClient
from . import Profiler, ProfilingResult

if typing.TYPE_CHECKING:
    from ...systems.connectors.sql_connector import SQLConnector


class GxProfiler(Profiler):
    connector: "SQLConnector"
    extension = "json"

    def profile_table(self) -> ProfilingResult:
        gx = GxClient()

        gx.add_datasource(table=self.profile.dbtable, connection_string=self.connector.sqla_connection_string)

        batch_request = gx.batch_request(table=self.profile.dbtable)
        validator = gx.context.get_validator(batch_request=batch_request)
        profiler = UserConfigurableProfiler(
            profile_dataset=validator,
            value_set_threshold="VERY_FEW",
            excluded_expectations=["expect_column_quantile_values_to_be_between"],
        )

        suite = profiler.build_suite()
        suite.expectation_suite_name = self.profile.dbtable.fullname
        gx.context.add_or_update_expectation_suite(
            expectation_suite=suite,
        )
        validator.save_expectation_suite(self.report_file_path)

        return ProfilingResult(
            rows=validator.get_metric(MetricConfiguration("table.row_count", {})),
            variables=validator.get_metric(MetricConfiguration("table.column_count", {})),
        )
