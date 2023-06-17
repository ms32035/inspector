from rest_framework import decorators, mixins, permissions, viewsets
from rest_framework.response import Response

from . import models, serializers


class TableProfileViewSet(mixins.DestroyModelMixin, viewsets.ReadOnlyModelViewSet):
    """ViewSet for the Datacheck class"""

    queryset = models.TableProfile.objects.all()
    serializer_class = serializers.TableProfileSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filterset_fields = ("dbtable",)

    @decorators.action(detail=True, methods=["get"])
    def report(self, request, pk):
        profile = models.TableProfile.objects.get(pk=pk)
        return Response({"id": pk, "data": profile.result.read(), "format": profile.result.name.split(".")[-1]})
