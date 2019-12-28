from django.conf import settings
from django.db import models

from ..base.constants import STATUSES
from ..systems.models import DbTable, System, Environment


class TableProfile(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    dbtable = models.ForeignKey(DbTable, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUSES.NEW)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.FileField(max_length=255)
    rows = models.IntegerField(null=True)

    class Meta:
        ordering = ("-pk",)
