from sqlalchemy.engine import reflection

from .connectors import Connector, get_connector_for_instance
from .models import Instance, DbTable


class MetadataService:
    def __init__(self, instance: Instance):
        self.instance = instance
        self.connector: Connector = get_connector_for_instance(instance)

    def compare_tables(self):
        self.connector.get_engine()
        self.connector.test_connection()
        tables = dict()
        insp = reflection.Inspector.from_engine(self.connector.engine)
        schemas = insp.get_schema_names()
        for schema in schemas:
            schema_tabs = insp.get_table_names(schema=schema)
            for tab in schema_tabs:
                tables[f"{schema}.{tab}"] = (schema, tab)

        db_tables = DbTable.objects.filter(system=self.instance.system)

        create_list = []

        for k, v in tables.items():
            if k not in db_tables.values_list("fullname", flat=True):
                create_list.append(
                    DbTable(
                        system=self.instance.system, fullname=k, schema=v[0], name=v[1]
                    )
                )
        DbTable.objects.bulk_create(create_list)

        # TO-DO: add removal
        # remove_list = [tab for tab in db_tables if tab.fullname not in tables.keys()]
