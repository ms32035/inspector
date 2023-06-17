from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TaggitSerializer, TagListSerializerField

from . import models


class DatacheckSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = models.Datacheck
        fields = "__all__"


class CheckRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CheckRun
        fields = "__all__"


class CheckRunCreateApiSerializer(serializers.Serializer):
    check_code = serializers.CharField(max_length=20, required=True, allow_blank=False)
    environment = serializers.CharField(max_length=50, required=True, allow_blank=False)


class DatacheckRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CheckRun
        fields = ("environment",)


class DatacheckRunByCodeSerializer(serializers.ModelSerializer):
    environment = serializers.CharField(max_length=50, required=True, allow_blank=False)

    class Meta:
        model = models.Datacheck
        fields = (
            "code",
            "environment",
        )


class TagSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class ExpectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expectation
        fields = "__all__"
