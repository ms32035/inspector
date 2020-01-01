Profiling
=========

The profiling modules generates table profile reports with Pandas Profiling,
tracks the profiling run history and can store the HTML reports in S3.

Pandas Profiling is suitable only for small to medium sized tables,
and for now only default report configuration is supported. A SQL profiler
capable of handling larger datasets might be added in the future.
