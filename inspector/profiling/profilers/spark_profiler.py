import logging

from pyspark.sql import SparkSession
from ydata_profiling import ProfileReport

from . import ProfilingResult
from .ydata_profiler import YDataProfiler

logger = logging.getLogger(__name__)


class SparkProfiler(YDataProfiler):
    def profile_table(self):
        spark_session = (
            SparkSession.builder.appName("SparkProfiling")
            .config("spark.jars.packages", self.connector.jar_package)
            .master("local[*]")
            .getOrCreate()
        )

        config = self.prepare_config()
        config.infer_dtypes = False
        config.correlations["pearson"].calculate = True
        config.correlations["spearman"].calculate = True
        config.interactions.continuous = False
        config.missing_diagrams["bar"] = False
        config.missing_diagrams["heatmap"] = False
        config.missing_diagrams["matrix"] = False

        logger.info("Loading table into DataFrame")
        df = spark_session.read.jdbc(
            url=self.connector.jdbc_connection_string,
            table=self.profile.dbtable.fullname,
            properties=self.connector.jdbc_options,
        )

        logger.info("Generating Spark Profiling report")
        profile_report = ProfileReport(df, title=self.report_file_name, config=config, **self.profile.parameters)

        logger.info("Saving profiling report: %s", self.report_file_path)
        profile_report.to_file(self.report_file_path)

        return ProfilingResult(rows=df.count(), variables=len(df.columns))
