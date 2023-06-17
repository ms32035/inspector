from .models import CheckRun, Datacheck


class CheckRunQuery:
    @staticmethod
    def get(**kwargs) -> "CheckRun":
        return CheckRun.objects.get(**kwargs)

    @staticmethod
    def datacheck_environment(checkrun_id: int) -> "CheckRun":
        return CheckRun.objects.select_related("datacheck").select_related("environment").get(id=checkrun_id)


class DatacheckQuery:
    @staticmethod
    def get(**kwargs) -> "Datacheck":
        return Datacheck.objects.get(**kwargs)
