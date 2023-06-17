from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from inspector.base.models import Statuses
from inspector.systems.models import Dataset, DbTable, Environment, Instance, System


class Expectation(models.Model):
    name = models.CharField(max_length=512, unique=True)
    class_name = models.CharField(max_length=1024, unique=True, null=True, blank=True)
    table_level = models.BooleanField(default=False)
    description = models.TextField(max_length=1024, null=True, blank=True)
    parameters = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Datacheck(models.Model):
    class Relations(models.TextChoices):
        EQ = "eq", _("=")
        NE = "ne", _("!=")
        GT = "gt", _(">")
        LT = "lt", _("<")
        GE = "ge", _(">=")
        LE = "le", _("<=")

    class CheckTypes(models.TextChoices):
        SQL_QUERY = "sql_query", _("SQL query")
        SQL_EXPRESSION = "sql_expression", _("SQL expression")
        NUMBER = "number", _("Number")
        STRING = "string", _("String")
        DATE = "date", _("Date")
        PYTHON_EXPRESSION = "python_expression", _("Python expression")
        EXPECTATION = "expectation", _("Expectation")

    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    weight = models.IntegerField(default=0)
    left_system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="left_system")
    left_type = models.CharField(max_length=30, choices=CheckTypes.choices[:2] + CheckTypes.choices[-1:])
    left_logic = models.TextField(null=True, blank=True)
    left_expectation = models.ForeignKey(Expectation, on_delete=models.CASCADE, null=True, blank=True)
    left_dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True, blank=True)
    left_column = models.CharField(max_length=256, null=True, blank=True)
    left_expectation_parameters = models.JSONField(null=True, blank=True)
    relation = models.CharField(max_length=5, choices=Relations.choices, null=True, blank=True)
    right_system = models.ForeignKey(
        System,
        on_delete=models.CASCADE,
        related_name="right_system",
        null=True,
        blank=True,
    )
    right_type = models.CharField(max_length=30, choices=CheckTypes.choices, null=True, blank=True)
    right_logic = models.TextField(null=True, blank=True)
    right_number_value = models.FloatField(null=True, blank=True)
    right_date_value = models.DateTimeField(null=True, blank=True)
    right_object_value = models.JSONField(null=True, blank=True)
    supports_warning = models.BooleanField(default=False)
    warning_relation = models.CharField(max_length=5, choices=Relations.choices, null=True, blank=True)
    warning_system = models.ForeignKey(
        System,
        on_delete=models.CASCADE,
        related_name="warning_system",
        null=True,
        blank=True,
    )
    warning_type = models.CharField(max_length=30, choices=CheckTypes.choices, null=True, blank=True)
    warning_logic = models.TextField(null=True, blank=True)
    warning_number_value = models.FloatField(null=True, blank=True)
    warning_date_value = models.DateTimeField(null=True, blank=True)
    warning_object_value = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ("-pk",)

    def clean(self):
        if self.left_type != self.CheckTypes.EXPECTATION:
            if self.left_logic is None:
                raise ValidationError(_("Left logic must be set"))
            if self.right_type is None:
                raise ValidationError(_("Right type must be set"))
            if self.relation is None:
                raise ValidationError(_("Relation must be set"))


class CheckRun(models.Model):
    class Results(models.TextChoices):
        SUCCESS = "success", _("Success")
        WARNING = "warning", _("Warning")
        FAILED = "failed", _("Failed")

    class ValueTypes(models.TextChoices):
        STRING = "string", _("String")
        NUMBER = "number", _("Number")
        DATE = "date", _("Date")
        OBJECT = "object", _("Object")

    datacheck = models.ForeignKey(Datacheck, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=Statuses.choices, default=Statuses.NEW)
    result = models.CharField(max_length=20, choices=Results.choices, null=True)
    left_instance = models.ForeignKey(Instance, on_delete=models.CASCADE, related_name="left_instance")
    left_value_type = models.CharField(max_length=20, choices=ValueTypes.choices)
    left_string_value = models.CharField(max_length=4096, null=True, blank=True)
    left_number_value = models.FloatField(null=True, blank=True)
    left_date_value = models.DateTimeField(null=True, blank=True)
    left_object_value = models.JSONField(null=True, blank=True)
    left_expectation = models.ForeignKey(Expectation, on_delete=models.CASCADE, null=True, blank=True)
    left_dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True, blank=True)
    left_table = models.ForeignKey(DbTable, on_delete=models.CASCADE, null=True, blank=True)
    left_column = models.CharField(max_length=256, null=True, blank=True)
    left_expectation_parameters = models.JSONField(null=True, blank=True)
    relation = models.CharField(max_length=5, choices=Datacheck.Relations.choices, null=True, blank=True)
    right_instance = models.ForeignKey(
        Instance, on_delete=models.CASCADE, related_name="right_instance", null=True, blank=True
    )
    right_value_type = models.CharField(max_length=20, choices=ValueTypes.choices, null=True, blank=True)
    right_string_value = models.CharField(max_length=4096, null=True, blank=True)
    right_number_value = models.FloatField(null=True, blank=True)
    right_date_value = models.DateTimeField(null=True, blank=True)
    right_object_value = models.JSONField(null=True, blank=True)
    warning_instance = models.ForeignKey(
        Instance, on_delete=models.CASCADE, related_name="warning_instance", null=True, blank=True
    )
    warning_relation = models.CharField(max_length=5, choices=Datacheck.Relations.choices, null=True, blank=True)
    warning_value_type = models.CharField(max_length=20, choices=ValueTypes.choices, null=True, blank=True)
    warning_string_value = models.CharField(max_length=4096, null=True, blank=True)
    warning_number_value = models.FloatField(null=True, blank=True)
    warning_date_value = models.DateTimeField(null=True, blank=True)
    warning_object_value = models.JSONField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-pk",)
