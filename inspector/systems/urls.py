from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r"system", api.SystemViewSet)
router.register(r"environment", api.EnvironmentViewSet)
router.register(r"instance", api.InstanceViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    path("api/v1/", include(router.urls)),
)

urlpatterns += (
    # urls for System
    path("system/", views.SystemListView.as_view(), name="system_list"),
    path("system/create/", views.SystemCreateView.as_view(), name="system_create",),
    path(
        "system/update/<int:pk>/",
        views.SystemUpdateView.as_view(),
        name="system_update",
    ),
    path(
        "system/delete/<int:pk>",
        views.SystemDeleteView.as_view(),
        name="system_delete",
    ),
)

urlpatterns += (
    # urls for Environment
    path("environment/", views.EnvironmentListView.as_view(), name="environment_list",),
    path(
        "environment/create/",
        views.EnvironmentCreateView.as_view(),
        name="environment_create",
    ),
    path(
        "environment/update/<int:pk>/",
        views.EnvironmentUpdateView.as_view(),
        name="environment_update",
    ),
    path(
        "environment/delete/<int:pk>",
        views.EnvironmentDeleteView.as_view(),
        name="environment_delete",
    ),
)

urlpatterns += (
    # urls for Instance
    path("instance/", views.InstanceListView.as_view(), name="instance_list",),
    path(
        "instance/create/", views.InstanceCreateView.as_view(), name="instance_create",
    ),
    path(
        "instance/detail/<int:pk>/",
        views.InstanceDetailView.as_view(),
        name="instance_detail",
    ),
    path(
        "instance/update/<int:pk>/",
        views.InstanceUpdateView.as_view(),
        name="instance_update",
    ),
    path(
        "instance/delete/<int:pk>/",
        views.InstanceDeleteView.as_view(),
        name="instance_delete",
    ),
    path(
        "instance/reflect/<int:pk>/",
        views.InstanceReflectView.as_view(),
        name="instance_reflect",
    ),
)

urlpatterns += (
    # urls for DBTable
    path("tables/", views.DbTableListView.as_view(), name="table_list",),
)
