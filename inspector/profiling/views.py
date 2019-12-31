from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages import success
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django_filters.views import BaseFilterView

from .filters import TableProfileFilter
from .models import TableProfile
from ..systems.models import DbTable
from ..taskapp.tasks import profile_table


class TableProfileCreateView(PermissionRequiredMixin, View):
    permission_required = "profiling.add_tableprofile"
    success_message = "Success: Profiling job was triggered."
    success_url = reverse_lazy("profiling:profile_list")

    def get(self, request, *args, **kwargs):
        profile = TableProfile(
            dbtable=DbTable.objects.get(id=self.kwargs["pk"]), user=request.user
        )
        profile.save()
        profile_table.delay(profile.id, "pandas")
        success(request, message=self.success_message)
        return redirect(self.success_url)


class TableProfileListView(PermissionRequiredMixin, BaseFilterView, ListView):
    permission_required = "profiling.view_tableprofile"
    paginate_by = 50
    filterset_class = TableProfileFilter

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_queryset(self):
        qs = TableProfile.objects.select_related()
        qs_filtered_list = TableProfileFilter(self.request.GET, queryset=qs)

        return qs_filtered_list.qs


class TableProfileDetailView(PermissionRequiredMixin, View):
    permission_required = "profiling.view_tableprofile"

    def get(self, request, *args, **kwargs):
        profile = TableProfile.objects.get(id=self.kwargs["pk"])
        return HttpResponse(profile.result.file)
