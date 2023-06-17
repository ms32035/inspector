from .connectors import Connector
from .models import Dataset, DbTable, Instance


class MetadataService:
    def __init__(self, instance: Instance):
        self.instance = instance
        self.connector: Connector = Connector.get_connector_for_instance(instance)

    def compare_tables(self):
        tables = self.connector.get_datasets()
        system = self.instance.system

        datasets = {x.fullname: x for x in Dataset.objects.filter(system=system)}

        new_datasets = Dataset.objects.bulk_create(
            [
                Dataset(system=system, name=v.name, schema=v.schema, db=v.db)
                for k, v in tables.items()
                if k not in datasets
            ]
        )

        for dts in new_datasets:
            datasets[dts.fullname] = dts

        db_tables = DbTable.all_objects.filter(instance=self.instance)

        for tab in db_tables:
            ref_table = tables.pop(tab.fullname, None)
            # in new
            if ref_table:
                # not in old - restore
                if tab.deleted:
                    tab.undelete()
            # not in old
            else:
                tab.delete()

        create_list = []

        # only new left now in tables
        for k, v in tables.items():
            create_list.append(
                DbTable(
                    instance=self.instance,
                    environment=self.instance.environment,
                    dataset=datasets[k],
                    system=system,
                    schema=v.schema,
                    name=v.name,
                )
            )
        DbTable.objects.bulk_create(create_list)
