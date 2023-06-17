from django.db import models
from django.utils.translation import gettext_lazy as _
from encrypted_model_fields.fields import EncryptedCharField
from safedelete.models import SOFT_DELETE, SafeDeleteModel


class System(models.Model):
    class Applications(models.TextChoices):
        POSTGRES = "postgres", _("Postgresql")
        REDSHIFT = "redshift", _("Redshift")
        MYSQL = "mysql", _("MySQL")
        SNOWFLAKE = (
            "snowflake",
            _("Snowflake"),
        )

    name = models.CharField(max_length=50, unique=True, null=True)
    application = models.CharField(max_length=30, choices=Applications.choices)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-pk",)


class Environment(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-pk",)


class Instance(models.Model):
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    environment = models.ForeignKey(Environment, on_delete=models.PROTECT)
    host = models.CharField(max_length=100, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    db = models.CharField(max_length=100, null=True, blank=True)
    schema = models.CharField(max_length=100, null=True, blank=True)
    login = models.CharField(max_length=100, null=True, blank=True)
    password = EncryptedCharField(max_length=100, null=True, blank=True)
    extra_json = models.JSONField(null=True, blank=True)
    unique_together = ((system, environment),)

    class Meta:
        ordering = ("-pk",)


class Dataset(models.Model):
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    db = models.CharField(max_length=255, null=True)
    schema = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    @property
    def fullname(self):
        name = []
        if self.db:
            name.append(self.db)
        if self.schema:
            name.append(self.schema)
        name.append(self.name)

        return ".".join(name)

    class Meta:
        ordering = ("system", "db", "schema", "name")
        unique_together = ("system", "db", "schema", "name")


class DbTable(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    system = models.ForeignKey(System, on_delete=models.PROTECT)
    environment = models.ForeignKey(Environment, on_delete=models.PROTECT)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    db = models.CharField(max_length=255, null=True)
    schema = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    last_profiling_at = models.DateTimeField(null=True)
    rows = models.IntegerField(null=True)

    class Meta:
        unique_together = ("instance", "db", "schema", "name")
        ordering = ("instance", "db", "schema", "name")

    @property
    def fullname(self):
        name = []
        if self.db:
            name.append(self.db)
        if self.schema:
            name.append(self.schema)
        name.append(self.name)

        return ".".join(name)

    def __str__(self):
        return self.fullname
