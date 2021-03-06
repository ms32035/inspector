from bootstrap_modal_forms.mixins import PassRequestMixin, DeleteMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages import success
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Max, Subquery
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
    FormView,
    View,
)
from django_filters.views import BaseFilterView

from inspector.taskapp.tasks import execute_check
from .filters import CheckRunFilter
from .forms import DatacheckRunForm, DatacheckForm, CheckRunTagForm
from .models import Datacheck, CheckRun
from .service import CheckRunService


class CheckListView(PermissionRequiredMixin, ListView):
    permission_required = "checks.view_datacheck"
    model = Datacheck
    slug_field = "code"
    slug_url_kwarg = "code"

    def get_queryset(self):
        return (
            Datacheck.objects.prefetch_related("tags")
            .select_related("left_system")
            .order_by("code")
        )


check_list_view = CheckListView.as_view()


class DatacheckDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "checks.view_datacheck"
    model = Datacheck
    template_name = "checks/datacheck_detail.html"


check_detail_view = DatacheckDetailView.as_view()


class DatacheckRunView(
    PermissionRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView
):
    permission_required = "checks.add_checkrun"
    template_name = "components/modals_run.html"
    form_class = DatacheckRunForm
    success_message = "Success: Check was triggered."
    success_url = reverse_lazy("checks:checkrun_list")

    def form_valid(self, form):
        form.instance.datacheck_id = self.kwargs["pk"]
        form.instance.user = self.request.user
        # TODO - check if system is available in environment

        return super().form_valid(form)

    def get_success_url(self):
        if not self.request.is_ajax():
            execute_check.delay(self.object.id)
        return super().get_success_url()


datacheck_run_view = DatacheckRunView.as_view()


class CheckRunRerunView(PermissionRequiredMixin, View):
    permission_required = "checks.add_checkrun"
    success_message = "Success: Check was retriggered."
    success_url = reverse_lazy("checks:checkrun_list")

    def get(self, request, *args, **kwargs):
        CheckRunService.checkrun_rerun(kwargs["pk"], request.user)
        success(request, self.success_message)
        return redirect(self.success_url)


class CheckRunTagView(
    PermissionRequiredMixin, PassRequestMixin, SuccessMessageMixin, FormView
):
    permission_required = "checks.add_checkrun"
    template_name = "components/modals_run.html"
    form_class = CheckRunTagForm
    success_message = "Success: Checks were triggered."
    success_url = reverse_lazy("checks:checkrun_list")

    def form_valid(self, form):
        if not self.request.is_ajax():
            CheckRunService.run_check_tag(
                form.cleaned_data["tag"], form.instance.environment, self.request.user
            )

        return super().form_valid(form)


class DatacheckDeleteView(PermissionRequiredMixin, DeleteMessageMixin, DeleteView):
    permission_required = "checks.delete_datacheck"
    model = Datacheck
    template_name = "components/modals_delete.html"
    success_message = "Success: Check was deleted."
    success_url = reverse_lazy("checks:datacheck_list")


check_delete_view = DatacheckDeleteView.as_view()


class CheckRunListView(PermissionRequiredMixin, BaseFilterView, ListView):
    permission_required = "checks.view_checkrun"
    model = CheckRun
    paginate_by = 50
    filterset_class = CheckRunFilter

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_queryset(self):
        qs = CheckRun.objects.select_related()
        qs_filtered_list = CheckRunFilter(self.request.GET, queryset=qs)

        return qs_filtered_list.qs


class CheckRunDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "checks.view_checkrun"
    model = CheckRun


class DatacheckCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "checks.add_datacheck"
    model = Datacheck
    form_class = DatacheckForm

    def get_success_url(self):
        return reverse("checks:datacheck_list")


class DatacheckUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "checks.change_datacheck"
    model = Datacheck
    form_class = DatacheckForm

    def get_success_url(self):
        return reverse("checks:datacheck_list")


class DatacheckInfoView(PermissionRequiredMixin, DetailView):
    permission_required = "checks.view_datacheck"
    model = Datacheck
    template_name = "checks/datacheck_info.html"


class CheckRunLatestListView(PermissionRequiredMixin, BaseFilterView, ListView):
    permission_required = "checks.view_checkrun"
    model = CheckRun
    paginate_by = 50
    filterset_class = CheckRunFilter

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_queryset(self):
        latest_id = (
            CheckRun.objects.values("datacheck_id", "environment_id")
            .annotate(max_id=Max("id"))
            .values("max_id")
        )
        qs = (
            CheckRun.objects.filter(id__in=Subquery(latest_id))
            .select_related()
            .order_by("environment__name", "datacheck__code")
        )
        qs_filtered_list = CheckRunFilter(self.request.GET, queryset=qs)

        return qs_filtered_list.qs
