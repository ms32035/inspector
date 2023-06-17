import logging

from ydata_profiling import ProfileReport

from . import ProfilingResult
from .ydata_profiler import YDataProfiler

logger = logging.getLogger(__name__)


class PandasProfiler(YDataProfiler):
    def profile_table(self):
        logger.info("Loading table into DataFrame")
        df = self.connector.table_df(table=self.profile.dbtable.name, schema=self.profile.dbtable.schema)

        self.profile.rows = len(df.index)
        logger.info("Generating Pandas Profiling report")
        profile_report = ProfileReport(
            df, title=self.report_file_name, config=self.prepare_config(), **self.profile.parameters
        )
        logger.info("Saving profiling report: %s", self.report_file_path)
        profile_report.to_file(self.report_file_path)

        return ProfilingResult(rows=len(df), variables=len(df.columns))
