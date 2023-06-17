from django.urls import include, path
from rest_framework import routers

from . import api

app_name = "checks"


router = routers.DefaultRouter()
router.register(r"datacheck", api.DatacheckViewSet)
router.register(r"checkrun", api.CheckRunViewSet)
router.register(r"tag", api.TagViewSet)
router.register(r"expectation", api.ExpectationViewSet)

urlpatterns = (path("v1/", include(router.urls)),)
