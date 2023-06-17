from django.urls import include, path
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register(r"system", api.SystemViewSet)
router.register(r"environment", api.EnvironmentViewSet)
router.register(r"instance", api.InstanceViewSet)
router.register(r"table", api.DbTableViewSet)
router.register(r"dataset", api.DatasetViewSet)

urlpatterns = (path("v1/", include(router.urls)),)

app_name = "systems"
