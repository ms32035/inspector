from rest_framework import serializers

from . import models


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.System
        fields = "__all__"


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Environment
        fields = "__all__"


class InstanceSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = models.Instance
        fields = "__all__"


class DBTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DbTable
        fields = "__all__"


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dataset
        fields = "__all__"


class ResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
