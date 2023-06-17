from django.urls import include, path
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register(r"profile", api.TableProfileViewSet)

urlpatterns = (path("v1/", include(router.urls)),)

app_name = "profiling"
