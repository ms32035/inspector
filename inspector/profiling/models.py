from django.conf import settings
from django.db import models

from ..base.models import Statuses
from ..systems.models import Dataset, DbTable


class TableProfile(models.Model):
    class Profilers(models.TextChoices):
        PANDAS = "pandas", "Pandas Profiler"
        SPARK = "spark", "Spark Profiler"
        GX = "gx", "GX Profiler"

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    dbtable = models.ForeignKey(DbTable, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=Statuses.choices, default=Statuses.NEW)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    profiler = models.CharField(max_length=20, choices=Profilers.choices, default=Profilers.PANDAS)
    parameters = models.JSONField(null=True, blank=True, default=dict)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.FileField(max_length=255, upload_to=settings.PROFILING_REPORTS_PATH)
    rows = models.IntegerField(null=True)
    variables = models.IntegerField(null=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self):
        return f"{self.dbtable.fullname} - {self.created_at}"
