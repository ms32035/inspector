from django import forms
from django.contrib import admin

from .models import TableProfile


class TableProfileAdminForm(forms.ModelForm):
    class Meta:
        model = TableProfile
        fields = "__all__"


class TableProfileAdmin(admin.ModelAdmin):
    form = TableProfileAdminForm
    list_select_related = ("dbtable",)


admin.site.register(TableProfile, TableProfileAdmin)
