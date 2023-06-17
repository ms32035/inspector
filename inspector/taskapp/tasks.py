from celery import shared_task

from ..checks.engine.processor import CheckProcessor
from ..profiling.models import TableProfile
from ..profiling.service import ProfilerService
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
def profile_table(profile_id: int):
    profile = TableProfile.objects.select_related("dbtable").get(id=profile_id)
    profiler = ProfilerService.get_profiler(profile)

    try:
        ProfilerService.begin_profiling(profile)
        ProfilerService.profile_table(profile, profiler)
        ProfilerService.save_report(profile, profiler)

    except Exception as exc:
        ProfilerService.save_error(profile, exc)
        raise (exc)
