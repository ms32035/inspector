from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import decorators, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from inspector.profiling.models import TableProfile
from inspector.profiling.serializers import TableProfileCreateSerializer, TableProfileSerializer

from ..base.api import NumberInFilter
from ..taskapp.tasks import profile_table, reflect_instance
from . import models, serializers


class SystemFilter(filters.FilterSet):
    id__in = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = models.System
        fields = ("id", "name")


class SystemViewSet(viewsets.ModelViewSet):
    """ViewSet for the System class"""

    queryset = models.System.objects.all()
    serializer_class = serializers.SystemSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filterset_class = SystemFilter


class EnvironmentFilter(filters.FilterSet):
    id__in = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = models.Environment
        fields = ("id", "name")


class EnvironmentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Environment class"""

    queryset = models.Environment.objects.all()
    serializer_class = serializers.EnvironmentSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filterset_class = EnvironmentFilter


class InstanceFilter(filters.FilterSet):
    id__in = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = models.Instance
        fields = ("id",)


class InstanceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Instance class"""

    queryset = models.Instance.objects.all()
    serializer_class = serializers.InstanceSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filterset_class = InstanceFilter

    def get_serializer_class(self):
        if self.action == "reflect":
            return Serializer
        else:
            return serializers.InstanceSerializer

    @extend_schema(request=None, responses={200: serializers.ResponseSerializer})
    @decorators.action(detail=True, methods=["post"])
    def reflect(self, request, pk=None):
        reflect_instance.delay(pk)
        return Response({"message": "OK"}, status=status.HTTP_200_OK)


class DbTableFilter(filters.FilterSet):
    id__in = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = models.DbTable
        fields = ("id", "instance", "schema", "name", "dataset")


class DbTableViewSet(viewsets.ModelViewSet):
    """ViewSet for the Table class"""

    queryset = models.DbTable.objects.all()
    serializer_class = serializers.DBTableSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filterset_class = DbTableFilter
    search_fields = ("name", "schema", "db")

    def get_serializer_class(self):
        if self.action == "profile":
            return TableProfileCreateSerializer
        else:
            return serializers.DBTableSerializer

    @decorators.action(detail=True, methods=["post"])
    def profile(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        profiler = data.pop("profiler")
        table = models.DbTable.objects.get(pk=pk)

        profile = TableProfile.objects.create(
            dataset=table.dataset, dbtable=table, user=request.user, profiler=profiler, parameters=data
        )
        profile.save()

        profile_table.delay(profile.pk)
        return Response(TableProfileSerializer(profile).data, status=status.HTTP_200_OK)


class DatasetFilter(filters.FilterSet):
    id__in = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = models.Dataset
        fields = ("id", "name")


class DatasetViewSet(viewsets.ReadOnlyModelViewSet, mixins.DestroyModelMixin):
    """ViewSet for the Dataset class"""

    queryset = models.Dataset.objects.all()
    serializer_class = serializers.DatasetSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filterset_class = DatasetFilter
    search_fields = ("name", "schema", "db")
