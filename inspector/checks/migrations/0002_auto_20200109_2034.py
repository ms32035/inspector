# Generated by Django 3.0.2 on 2020-01-09 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="checkrun",
            name="left_value",
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
        migrations.AlterField(
            model_name="checkrun",
            name="right_value",
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
        migrations.AlterField(
            model_name="checkrun",
            name="warning_value",
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
    ]
