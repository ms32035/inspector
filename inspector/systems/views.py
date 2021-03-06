from bootstrap_modal_forms.mixins import DeleteMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages import success
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.debug import sensitive_variables
from django.views.generic import (
    DetailView,
    ListView,
    UpdateView,
    CreateView,
    DeleteView,
    View,
)
from django_filters.views import BaseFilterView

from .filters import DbTableFilter
from .forms import SystemForm, EnvironmentForm, InstanceForm
from .models import System, Environment, Instance, DbTable
from ..taskapp.tasks import reflect_instance


class SystemListView(PermissionRequiredMixin, ListView):
    permission_required = "systems.view_system"
    model = System


class SystemCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "systems.add_system"
    model = System
    form_class = SystemForm

    def get_success_url(self):
        return reverse("systems:system_list")


class SystemUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "systems.change_system"
    model = System
    form_class = SystemForm

    def get_success_url(self):
        return reverse("systems:system_list")


class EnvironmentListView(PermissionRequiredMixin, ListView):
    permission_required = "systems.view_environment"
    model = Environment


class EnvironmentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "systems.add_environment"
    model = Environment
    form_class = EnvironmentForm

    def get_success_url(self):
        return reverse("systems:environment_list")


class EnvironmentUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "systems.change_environment"
    model = Environment
    form_class = EnvironmentForm

    def get_success_url(self):
        return reverse("systems:environment_list")


class InstanceListView(PermissionRequiredMixin, ListView):
    permission_required = "systems.view_instance"
    model = Instance

    def get_queryset(self):
        return Instance.objects.select_related()


class InstanceCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "systems.add_instance"
    model = Instance
    form_class = InstanceForm

    @sensitive_variables("new_password")
    def form_valid(self, form):
        clean = form.cleaned_data
        new_password = clean.get("new_password")
        form.instance.password = new_password
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("systems:instance_list")


class InstanceDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "systems.view_instance"
    model = Instance


class InstanceUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "systems.change_instance"

    model = Instance
    form_class = InstanceForm

    @sensitive_variables("new_password")
    def form_valid(self, form):
        clean = form.cleaned_data
        new_password = clean.get("new_password")
        if new_password:
            form.instance.password = new_password
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("systems:instance_list")


class SystemDeleteView(PermissionRequiredMixin, DeleteMessageMixin, DeleteView):
    permission_required = "systems.delete_system"
    model = System
    template_name = "components/modals_delete.html"
    success_message = "Success: System was deleted."
    success_url = reverse_lazy("systems:system_list")


class EnvironmentDeleteView(PermissionRequiredMixin, DeleteMessageMixin, DeleteView):
    permission_required = "systems.delete_environment"
    model = Environment
    template_name = "components/modals_delete.html"
    success_message = "Success: Environment was deleted."
    success_url = reverse_lazy("systems:environment_list")


class InstanceDeleteView(PermissionRequiredMixin, DeleteMessageMixin, DeleteView):
    permission_required = "systems.delete_instance"
    model = Instance
    template_name = "components/modals_delete.html"
    success_message = "Success: Instance was deleted."
    success_url = reverse_lazy("systems:instance_list")


class DbTableListView(PermissionRequiredMixin, BaseFilterView, ListView):
    permission_required = "systems.view_dbtable"
    paginate_by = 50
    filterset_class = DbTableFilter

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_queryset(self):
        qs = DbTable.objects.select_related()
        qs_filtered_list = DbTableFilter(self.request.GET, queryset=qs)

        return qs_filtered_list.qs


class InstanceReflectView(PermissionRequiredMixin, View):
    permission_required = "systems.add_dbtable"
    success_message = "Success: Reflection job started."
    success_url = reverse_lazy("systems:table_list")

    def get(self, request, *args, **kwargs):
        reflect_instance.delay(kwargs["pk"])
        success(request, self.success_message)
        return redirect(self.success_url)
