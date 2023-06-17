from rest_framework import serializers

from . import models


class TableProfileCreateSerializer(serializers.Serializer):
    profiler = serializers.CharField()
    minimal = serializers.BooleanField(required=False)


class TableProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TableProfile
        fields = "__all__"
