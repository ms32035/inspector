from bootstrap_modal_forms.forms import BSModalForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, HTML
from django import forms

from .models import TableProfile
from ..base.constants import SUBMIT_CSS_CLASSES
from ..base.forms import prepended_select_column


class TableProfileRunForm(BSModalForm):
    class Meta:
        model = TableProfile
        fields = ["environment"]


class TableProfileFilterForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "GET"
    helper.layout = Layout(
        Row(
            prepended_select_column("system", 4, "mb-1"),
            prepended_select_column("environment", 3, "mb-1"),
            prepended_select_column("status", 2, "mb-1"),
            prepended_select_column("user", 3, "mb-1"),
        ),
        Row(
            prepended_select_column("dbtable", 6, "mb-1"),
            Column(
                Submit("submit", "Search", css_class=SUBMIT_CSS_CLASSES),
                css_class="form-group col-md-1 mb-1",
            ),
            Column(
                HTML(
                    """
                <a class="btn btn-outline-danger btn-block btn-sm"
                href={% url "profiling:profile_list" %}>Reset</a>
                """
                ),
                css_class="form-group col-md-1 mb-1",
            ),
            css_class="form-row",
        ),
    )

    class Meta:
        model = TableProfile
        fields = ["system", "environment", "dbtable", "user", "status"]
