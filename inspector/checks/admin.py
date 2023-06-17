from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import JSON
from import_export.widgets import ForeignKeyWidget, Widget

from .models import Datacheck, Expectation, System


class TaggitTagsReadonlyWidget(Widget):
    def __init__(self, separator=",", *args, **kwargs):
        self.separator = separator

    def render(self, value, obj=None):
        return self.separator.join([tag.name for tag in value.all()])

    def clean(self, value, row=None, *args, **kwargs):
        raise NotImplementedError("Use readonly=True on the tags field.")


class DatacheckResource(resources.ModelResource):
    left_system = fields.Field(
        column_name="left_system",
        attribute="left_system",
        widget=ForeignKeyWidget(System, "name"),
    )

    right_system = fields.Field(
        column_name="right_system",
        attribute="right_system",
        widget=ForeignKeyWidget(System, "name"),
    )

    tags = fields.Field(
        column_name="tags",
        attribute="tags",
        widget=TaggitTagsReadonlyWidget(),
        readonly=True,
    )

    class Meta:
        model = Datacheck
        import_id_fields = ["code"]
        exclude = ["id"]
        fields = [
            "code",
            "description",
            "tags",
            "weight",
            "left_system",
            "left_type",
            "left_logic",
            "relation",
            "right_system",
            "right_type",
            "right_logic",
            "supports_warning",
            "warning_relation",
            "warning_type",
            "warning_logic",
        ]

    def after_import_row(self, row, row_result, **kwargs):
        instance = self._meta.model.objects.get(pk=row_result.object_id)
        instance.tags.set(*row["tags"].split(","))


class DatacheckAdmin(ImportExportModelAdmin):
    fieldsets = (
        (None, {"fields": ("code", "description", "tags", "weight")}),
        ("Left", {"fields": ("left_system", "left_type", "left_logic")}),
        ("Relation", {"fields": ("relation",)}),
        ("Right", {"fields": ("right_system", "right_type", "right_logic")}),
        ("Warning", {"fields": ("supports_warning", "warning_type", "warning_logic")}),
    )
    resource_class = DatacheckResource
    formats = (JSON,)


admin.site.register(Datacheck, DatacheckAdmin)


class ExpectationResource(resources.ModelResource):
    class Meta:
        model = Expectation
        import_id_fields = ("name",)

        fields = ("name", "description", "table_level")


class ExpectationAdmin(ImportExportModelAdmin):
    resource_class = ExpectationResource


admin.site.register(Expectation, ExpectationAdmin)
