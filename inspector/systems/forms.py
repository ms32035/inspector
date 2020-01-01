from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms

from .models import Environment, Instance, System, DbTable
from ..base.components import button_reset
from ..base.constants import SUBMIT_CSS_CLASSES
from ..base.forms import prepended_select_column


class SystemForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit", css_class=SUBMIT_CSS_CLASSES))

    class Meta:
        model = System
        fields = ["name", "application"]


class EnvironmentForm(forms.ModelForm):
    class Meta:
        model = Environment
        fields = ["name"]

    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit", css_class=SUBMIT_CSS_CLASSES))


class InstanceForm(forms.ModelForm):
    class Meta:
        model = Instance
        fields = [
            "system",
            "environment",
            "host",
            "port",
            "db",
            "schema",
            "login",
            "extra_json",
        ]
        widgets = {
            "extra_json": forms.Textarea({"cols": 40, "rows": 3}),
        }

    new_password = forms.CharField(
        required=False, widget=forms.widgets.PasswordInput, label="Password"
    )

    helper = FormHelper()
    helper.layout = Layout(
        Row(
            Column("system", css_class="form-group col-md-6 mb-0"),
            Column("environment", css_class="form-group col-md-6 mb-0"),
            css_class="form-row",
        ),
        Row(
            Column("host", css_class="form-group col-md-10 mb-0"),
            Column("port", css_class="form-group col-md-2 mb-0"),
            css_class="form-row",
        ),
        Row(
            Column("db", css_class="form-group col-md-6 mb-0"),
            Column("schema", css_class="form-group col-md-6 mb-0"),
            css_class="form-row",
        ),
        Row(
            Column("login", css_class="form-group col-md-6 mb-0"),
            Column("new_password", css_class="form-group col-md-6 mb-0"),
            css_class="form-row",
        ),
        Row(
            Column("extra_json", css_class="form-group col-md-12 mb-0"),
            css_class="form-row",
        ),
        Submit("submit", "Submit", css_class="btn-sm"),
    )


class DbTableFilterForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "GET"
    helper.layout = Layout(
        Row(
            prepended_select_column("system", 4, "mb-1"),
            prepended_select_column("environment", 4, "mb-1"),
            prepended_select_column("schema", 2, "mb-1"),
            Column(
                Submit("submit", "Search", css_class=SUBMIT_CSS_CLASSES),
                css_class="form-group col-md-1 mb-1",
            ),
            Column(
                button_reset("checks_checkrun_list"),
                css_class="form-group col-md-1 mb-1",
            ),
        )
    )

    class Meta:
        model = DbTable
        fields = ["system", "environment", "schema"]
