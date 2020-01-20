from rest_framework import viewsets, permissions, authentication, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from . import models
from . import serializers
from .service import CheckRunService
from ..base.api import AuthPermission


class DatacheckViewSet(viewsets.ModelViewSet):
    """ViewSet for the Datacheck class"""

    queryset = models.Datacheck.objects.all()
    serializer_class = serializers.DatacheckSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class CheckRunViewSet(viewsets.ModelViewSet):
    """ViewSet for the CheckRun class"""

    queryset = models.CheckRun.objects.all()
    serializer_class = serializers.CheckRunSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class DatacheckRunPermission(AuthPermission):
    authenticated_users_only = True
    perms = "checks.add_checkrun"


class RunCheck(CreateAPIView):
    """
    Run a single check in and environment
    """

    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (DatacheckRunPermission,)
    serializer_class = serializers.CheckRunCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            checkrun_id = CheckRunService.create_check_run_api(
                serializer["check_code"].value,
                serializer["environment"].value,
                request.user,
            )
        except (models.Datacheck.DoesNotExist, models.Environment.DoesNotExist) as exc:
            return Response(str(exc), status=400)

        return Response({"checkrun_id": checkrun_id}, status=status.HTTP_200_OK)


class RunCheckTag(CreateAPIView):
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (DatacheckRunPermission,)
    serializer_class = serializers.CheckRunTagCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            CheckRunService.run_check_tag(
                serializer["checkgroup_name"].value,
                serializer["environment"].value,
                request.user,
            )
        except models.Environment.DoesNotExist as exc:
            return Response(str(exc), status=400)

        return Response({serializer["tag"].value: "success"}, status=status.HTTP_200_OK)
