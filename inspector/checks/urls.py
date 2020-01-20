from django.urls import path, include
from rest_framework import routers

from inspector.checks.views import (
    check_list_view,
    check_detail_view,
    check_delete_view,
    datacheck_run_view,
)
from . import api
from . import views

router = routers.DefaultRouter()

urlpatterns = (
    # urls for Django Rest Framework API
    path("api/v1/", include(router.urls)),
    path("api/v1/runcheck/", api.RunCheck.as_view()),
)

urlpatterns += (
    # urls for CheckRun
    path("checkrun/", views.CheckRunListView.as_view(), name="checkrun_list",),
    path("checkrun/create/", views.DatacheckRunView.as_view(), name="checkrun_create",),
    path(
        "checkrun/detail/<int:pk>/",
        views.CheckRunDetailView.as_view(),
        name="checkrun_detail",
    ),
    path(
        "checkrun/rerun/<int:pk>/",
        views.CheckRunRerunView.as_view(),
        name="checkrun_rerun",
    ),
    path("checkrun/runtag/", views.CheckRunTagView.as_view(), name="checkrun_runtag",),
)

urlpatterns += (
    path("datacheck/", view=check_list_view, name="datacheck_list"),
    path(
        "datacheck/detail/<int:pk>/", view=check_detail_view, name="datacheck_detail",
    ),
    path(
        "datacheck/info/<int:pk>/",
        view=views.DatacheckInfoView.as_view(),
        name="datacheck_info",
    ),
    path("datacheck/delete/<int:pk>", check_delete_view, name="datacheck_delete",),
    path("datacheck/run/<int:pk>", datacheck_run_view, name="datacheck_run"),
    path(
        "datacheck/create/",
        views.DatacheckCreateView.as_view(),
        name="datacheck_create",
    ),
    path(
        "datacheck/update/<int:pk>/",
        views.DatacheckUpdateView.as_view(),
        name="datacheck_update",
    ),
)

urlpatterns += (
    path(
        "environment_status",
        views.CheckRunLatestListView.as_view(),
        name="datacheck_status",
    ),
)
