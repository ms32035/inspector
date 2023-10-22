from django.db.models import Max
from django_filters import rest_framework as filters
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import decorators, mixins, permissions, status, viewsets
from rest_framework.response import Response
from taggit.models import Tag

from ..base.api import AuthPermission, EmptySerializer, NumberInFilter
from . import models, serializers
from .engine.exceptions import InstanceNotFound
from .service import CheckRunService


class DatacheckRunPermission(AuthPermission):
    authenticated_users_only = True
    perms = "checks.add_checkrun"


class TagsFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(tags__name__in=[value])

        return qs


class DatacheckFilterSet(filters.FilterSet):
    tag = TagsFilter()
    id__in = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = models.Datacheck
        fields = (
            "code",
            "tag",
            "supports_warning",
        )


class DatacheckViewSet(viewsets.ModelViewSet):
    """ViewSet for the Datacheck class"""

    queryset = models.Datacheck.objects.all()
    permission_classes = [permissions.DjangoModelPermissions]
    filterset_class = DatacheckFilterSet
    ordering_fields = "__all__"
    ordering = ("code",)

    def get_serializer_class(self):
        if self.action == "run":
            return serializers.DatacheckRunSerializer
        elif self.action == "run_by_code":
            return serializers.DatacheckRunByCodeSerializer
        return serializers.DatacheckSerializer

    @decorators.action(detail=True, methods=["post"], permission_classes=[DatacheckRunPermission])
    def run(self, request, pk: int):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            checkrun = CheckRunService.create_check_run(
                pk,
                serializer["environment"].value,
                request.user,
            )
        except models.Datacheck.DoesNotExist:
            return Response({"message": "Datacheck not found"}, status=400)
        except models.Environment.DoesNotExist:
            return Response({"message": "Environment not found"}, status=400)
        except InstanceNotFound:
            return Response({"message": "Instance not found"}, status=400)

        return Response(serializers.CheckRunSerializer(checkrun).data)

    @decorators.action(detail=False, methods=["post"], permission_classes=[DatacheckRunPermission])
    def run_by_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            checkrun = CheckRunService.create_check_run_api(
                serializer["code"].value,
                serializer["environment"].value,
                request.user,
            )
        except models.Datacheck.DoesNotExist:
            return Response({"message": "Datacheck not found"}, status=400)
        except models.Environment.DoesNotExist:
            return Response({"message": "Environment not found"}, status=400)
        except InstanceNotFound:
            return Response({"message": "Instance not found"}, status=400)

        return Response(serializers.CheckRunSerializer(checkrun).data)


class CheckRunFilter(filters.FilterSet):
    id__in = NumberInFilter(field_name="id", lookup_expr="in")
    last_run = filters.BooleanFilter(method="last_run_filter")

    def last_run_filter(self, queryset, name, value):
        if value:
            return queryset.filter(
                id__in=models.CheckRun.objects.values("datacheck_id", "environment_id")
                .annotate(last_run=Max("id"))
                .values("last_run")
            )
        return queryset

    class Meta:
        model = models.CheckRun
        fields = ("id", "datacheck", "environment", "status", "result", "last_run")


class CheckRunViewSet(viewsets.ReadOnlyModelViewSet, mixins.DestroyModelMixin):
    """ViewSet for the CheckRun class"""

    queryset = models.CheckRun.objects.all()

    permission_classes = [permissions.DjangoModelPermissions]
    ordering_fields = "__all__"
    ordering = ("-created_at",)
    filterset_class = CheckRunFilter

    def get_serializer_class(self):
        if self.action == "rerun":
            return EmptySerializer
        return serializers.CheckRunSerializer

    @extend_schema(request=None)
    @decorators.action(detail=True, methods=["post"])
    def rerun(self, request, pk: int):
        new_run = CheckRunService.checkrun_rerun(pk, request.user)
        return Response(serializers.CheckRunSerializer(new_run).data)


class TagFilter(filters.FilterSet):
    id__in = filters.BaseInFilter(field_name="name", lookup_expr="in")

    class Meta:
        model = Tag
        fields = ("id", "name")


@extend_schema(parameters=[OpenApiParameter("id", OpenApiTypes.STR, OpenApiParameter.PATH)])
class TagViewSet(viewsets.ModelViewSet):
    """
    Not using taggit_serializer.serializers.TaggitSerializer because that's for listing
    tags for an instance of a model
    """

    queryset = Tag.objects.all().order_by("name")
    filterset_class = TagFilter

    def get_serializer_class(self):
        if self.action == "run":
            return serializers.DatacheckRunSerializer
        return serializers.TagSerializer

    def get_object(self):
        return Tag.objects.get(name=self.kwargs["pk"])

    @decorators.action(detail=True, methods=["post"], permission_classes=[DatacheckRunPermission])
    def run(self, request, pk: str):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            runs = CheckRunService.run_check_tag(
                Tag(name=pk),
                serializer["environment"].value,
                request.user,
            )
        except models.Environment.DoesNotExist:
            return Response({"message": "Environment not found"}, status=400)
        if not runs:
            return Response({"message": "No checks found for tag"}, status=400)

        return Response({"data": serializers.CheckRunSerializer(runs[0]).data}, status=status.HTTP_200_OK)


class ExpectationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Expectation class"""

    queryset = models.Expectation.objects.all()
    serializer_class = serializers.ExpectationSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    ordering_fields = "__all__"
