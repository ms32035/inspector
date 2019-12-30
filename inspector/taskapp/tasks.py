from celery import shared_task

from ..checks.engine.processor import CheckProcessor
from ..profiling.models import TableProfile
from ..profiling.service import PandasProfilerService
from ..systems.models import Instance
from ..systems.service import MetadataService


@shared_task
def execute_check(checkrun_id: int):
    processor = CheckProcessor(checkrun_id)
    prepare = processor.prepare_check()
    if prepare:
        processor.execute_checks()


@shared_task()
def reflect_instance(instance_id: int):
    instance = Instance.objects.get(id=instance_id)
    meta = MetadataService(instance)
    meta.compare_tables()


@shared_task
def profile_table(profile_id, profiler: str):
    profile = TableProfile.objects.get(id=profile_id)
    profiler = PandasProfilerService(profile=profile)
    profiler.start_profiling()
    profiler.profile_table()
    profiler.save_report()
    profiler.save_profile()
