import tablib
from django.core.management.base import BaseCommand
from pkg_resources import resource_filename

from ...admin import ExpectationResource


class Command(BaseCommand):
    help = "Import reference data"

    def add_arguments(self, parser):
        parser.add_argument("type", choices=["expectations"], help="Type of data to import", default="expectations")

    def handle(self, *args, **options):
        data_file = resource_filename("inspector.checks", f"data/{options['type']}.json")

        with open(data_file) as src:
            data = tablib.Dataset().load(src, format="json")

        ExpectationResource().import_data(data)
