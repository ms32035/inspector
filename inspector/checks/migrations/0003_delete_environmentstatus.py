# Generated by Django 3.0.2 on 2020-01-18 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("checks", "0002_auto_20200109_2034"),
    ]

    operations = [
        migrations.DeleteModel(name="EnvironmentStatus",),
    ]
