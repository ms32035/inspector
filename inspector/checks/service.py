from django.contrib.auth.models import User
from django.db import transaction

from inspector.taskapp.tasks import execute_check
from .models import Datacheck, Environment, CheckRun


class CheckRunService:
    @staticmethod
    def create_check_run_api(check_code: str, environment: str, user: User) -> int:
        datacheck = Datacheck.objects.get(code=check_code)
        environment = Environment.objects.get(name=environment)

        return CheckRunService._create_and_execute_checkrun(
            datacheck, environment, user
        )

    @staticmethod
    def run_check_tag(tag: str, environment: str, user: User):
        environment = Environment.objects.get(name=environment)

        for chk in Datacheck.objects.filter(tags__name__in=tag):
            CheckRunService._create_and_execute_checkrun(chk, environment, user)

    @staticmethod
    def _create_and_execute_checkrun(
        check: Datacheck, environment: Environment, user: User
    ) -> int:
        check_run = CheckRun(datacheck=check, environment=environment, user=user)
        with transaction.atomic():
            check_run.save()
            transaction.on_commit(lambda: execute_check.delay(check_run.id))

        return check_run.id
