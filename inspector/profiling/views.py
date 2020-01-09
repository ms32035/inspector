from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django_filters.views import BaseFilterView

from .filters import TableProfileFilter
from .forms import TableProfileRunForm
from .models import TableProfile
from ..taskapp.tasks import profile_table


class TableProfileCreateView(PermissionRequiredMixin, BSModalCreateView):
    permission_required = "profiling.add_tableprofile"
    success_message = "Success: Profiling job was triggered."
    success_url = reverse_lazy("profiling:profile_list")
    template_name = "components/modals_run.html"
    form_class = TableProfileRunForm

    def form_valid(self, form):
        form.instance.dbtable_id = self.kwargs["pk"]
        self.kwargs["mode"] = form.data["mode"]
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if not self.request.is_ajax():
            profile_table.delay(self.object.id, self.kwargs["mode"])
        return super().get_success_url()


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
