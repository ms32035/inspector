from django.conf import settings
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

from inspector.systems.models import Environment, System
from .constants import RELATIONS, RESULTS, CHECK_TYPES
from ..base.constants import STATUSES


class Datacheck(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    weight = models.IntegerField(default=0)
    left_system = models.ForeignKey(
        System, on_delete=models.CASCADE, related_name="left_system"
    )
    left_type = models.IntegerField(choices=CHECK_TYPES)
    left_logic = models.TextField()
    relation = models.IntegerField(choices=RELATIONS)
    right_system = models.ForeignKey(
        System,
        on_delete=models.CASCADE,
        related_name="right_system",
        null=True,
        blank=True,
    )
    right_type = models.IntegerField(choices=CHECK_TYPES)
    right_logic = models.TextField()
    supports_warning = models.BooleanField(default=False)
    warning_relation = models.IntegerField(choices=RELATIONS, null=True, blank=True)
    warning_type = models.IntegerField(choices=CHECK_TYPES, null=True, blank=True)
    warning_logic = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ("-pk",)

    def __unicode__(self):
        return "%s" % self.pk

    def get_url(self, action):
        return reverse(f"checks:datacheck_{action}", args=(self.pk,))

    def get_name(self):
        return self.code


class CheckRun(models.Model):
    datacheck = models.ForeignKey(Datacheck, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUSES.NEW)
    result = models.CharField(max_length=20, choices=RESULTS, null=True)
    left_value = models.CharField(max_length=4096, null=True, blank=True)
    right_value = models.CharField(max_length=4096, null=True, blank=True)
    warning_value = models.CharField(max_length=4096, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-pk",)

    def __unicode__(self):
        return "%s" % self.pk

    def get_url(self, action):
        return reverse(f"checks:checkrun_{action}", args=(self.pk,))
