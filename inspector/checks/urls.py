from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

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
    path("apidocs/", include_docs_urls(title="Inspector API")),
)

urlpatterns += (
    # urls for CheckRun
    path(
        "checks/checkrun/",
        views.CheckRunListView.as_view(),
        name="checks_checkrun_list",
    ),
    path(
        "checks/checkrun/create/",
        views.DatacheckRunView.as_view(),
        name="checks_checkrun_create",
    ),
    path(
        "checks/checkrun/detail/<int:pk>/",
        views.CheckRunDetailView.as_view(),
        name="checks_checkrun_detail",
    ),
    path(
        "checks/checkrun/rerun/<int:pk>/",
        views.CheckRunRerunView.as_view(),
        name="checks_checkrun_rerun",
    ),
    path(
        "checks/checkrun/runtag/",
        views.CheckRunTagView.as_view(),
        name="check_checkrun_runtag",
    ),
)

urlpatterns += (
    path("checks/datacheck/", view=check_list_view, name="checks_datacheck_list"),
    path(
        "checks/datacheck/detail/<int:pk>/",
        view=check_detail_view,
        name="checks_datacheck_detail",
    ),
    path(
        "checks/datacheck/info/<int:pk>/",
        view=views.DatacheckInfoView.as_view(),
        name="checks_datacheck_info",
    ),
    path(
        "checks/datacheck/delete/<int:pk>",
        check_delete_view,
        name="checks_datacheck_delete",
    ),
    path(
        "checks/datacheck/run/<int:pk>", datacheck_run_view, name="checks_datacheck_run"
    ),
    path(
        "checks/datacheck/create/",
        views.DatacheckCreateView.as_view(),
        name="checks_datacheck_create",
    ),
    path(
        "checks/datacheck/update/<int:pk>/",
        views.DatacheckUpdateView.as_view(),
        name="checks_datacheck_update",
    ),
)

urlpatterns += (
    # urls for EnvironmentStatus
    path(
        "checks/environmentstatus/",
        views.EnvironmentStatusListView.as_view(),
        name="checks_environmentstatus_list",
    ),
    path(
        "checks/environmentstatus/rerun/<int:pk>/",
        views.EnvironmentStatusRerunView.as_view(),
        name="checks_environmentstatus_rerun",
    ),
)
