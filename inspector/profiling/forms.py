from bootstrap_modal_forms.forms import BSModalForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms

from .models import TableProfile
from ..base.components import button_reset
from ..base.constants import SUBMIT_CSS_CLASSES
from ..base.forms import prepended_select_column


class TableProfileFilterForm(forms.Form):
    helper = FormHelper()
    helper.form_method = "GET"
    helper.layout = Layout(
        Row(
            prepended_select_column("dbtable__system", 4, "mb-1"),
            prepended_select_column("dbtable__environment", 3, "mb-1"),
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
                button_reset("profiling:profile_list"),
                css_class="form-group col-md-1 mb-1",
            ),
            css_class="form-row",
        ),
    )

    class Meta:
        model = TableProfile
        fields = [
            "dbtable__system",
            "dbtable__environment",
            "dbtable",
            "user",
            "status",
        ]


class TableProfileRunForm(BSModalForm):
    mode = forms.ChoiceField(
        label="Profiling mode",
        choices=[
            ("pandas_minimal", "Pandas - minimal"),
            ("pandas_full", "Pandas - full"),
        ],
    )

    class Meta:
        model = TableProfile
        fields = []
