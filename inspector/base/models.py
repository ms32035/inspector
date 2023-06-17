from django.db import models
from django.utils.translation import gettext_lazy as _


class Statuses(models.TextChoices):
    NEW = "new", _("New")
    RUNNING = "running", _("Running")
    FINISHED = "finished", _("Finished")
    ERROR = "error", _("Error")
