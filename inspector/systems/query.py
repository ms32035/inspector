from .models import DbTable, Environment, Instance, System


class InstanceNotFound(Exception):
    def __init__(self, system, environment):
        super().__init__(f"No instance for system [{system.name}] in environment [{environment.name}]")


class InstanceQuery:
    @staticmethod
    def get(**kwargs) -> "Instance":
        return Instance.objects.get(**kwargs)

    @staticmethod
    def system_environment(system_id: int, environment_id: int) -> "Instance":
        try:
            return Instance.objects.get(environment_id=environment_id, system=system_id)
        except Instance.DoesNotExist:
            raise InstanceNotFound(System.objects.get(pk=system_id), Environment.objects.get(pk=environment_id))


class EnvironmentQuery:
    @staticmethod
    def get(**kwargs) -> "Environment":
        return Environment.objects.get(**kwargs)


class DbTableQuery:
    @staticmethod
    def dataset_environment(dataset_id: int, environment_id: int) -> "DbTable":
        return DbTable.objects.get(dataset_id=dataset_id, environment_id=environment_id)
