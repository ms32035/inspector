from django.contrib.auth.models import User
from taggit.models import Tag
from django.db import transaction

from inspector.taskapp.tasks import execute_check
from .models import Datacheck, Environment, CheckRun, EnvironmentStatus


class CheckRunService:
    @staticmethod
    def create_check_run_api(check_code: str, environment: str, user: User) -> int:
        datacheck = Datacheck.objects.get(code=check_code)
        environment = Environment.objects.get(name=environment)

        return CheckRunService.create_and_execute_checkrun(datacheck, environment, user)

    @staticmethod
    def run_check_tag(tag: Tag, environment: str, user: User):
        environment = Environment.objects.get(name=environment)

        for chk in Datacheck.objects.filter(tags__name__in=tag.name):
            CheckRunService.create_and_execute_checkrun(chk, environment, user)

    @staticmethod
    def create_and_execute_checkrun(
        check: Datacheck, environment: Environment, user: User
    ) -> int:
        check_run = CheckRun(datacheck=check, environment=environment, user=user)
        with transaction.atomic():
            check_run.save()
            transaction.on_commit(lambda: execute_check.delay(check_run.id))

        return check_run.id

    @staticmethod
    def checkrun_rerun(ckeckrun_id: int, user: User):
        checkrun: CheckRun = CheckRun.objects.get(id=ckeckrun_id)
        CheckRunService.create_and_execute_checkrun(
            check=checkrun.datacheck, environment=checkrun.environment, user=user
        )


class EnvironmentStatusService:
    @staticmethod
    def env_status_rerun(status_id: int, user: User):
        env_status: EnvironmentStatus = EnvironmentStatus.objects.get(id=status_id)

        CheckRunService.create_and_execute_checkrun(
            check=env_status.datacheck, environment=env_status.environment, user=user
        )
