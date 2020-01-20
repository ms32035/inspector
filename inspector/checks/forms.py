from bootstrap_modal_forms.forms import BSModalForm
from crispy_forms.bootstrap import TabHolder, Tab, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms
from djangocodemirror.widgets import CodeMirrorWidget
from taggit.models import Tag

from .models import Datacheck, CheckRun
from ..base.components import fa_icon, button_reset
from ..base.constants import SUBMIT_CSS_CLASSES
from ..base.forms import prepended_select_column


class DatacheckRunForm(BSModalForm):
    class Meta:
        model = CheckRun
        fields = ["environment"]


class CheckRunTagForm(BSModalForm):
    tag = forms.ModelChoiceField(queryset=Tag.objects.all().order_by("name"))

    class Meta:
        model = CheckRun
        fields = ["environment"]


class DatacheckForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        Row(
            Column(
                PrependedText(
                    "code",
                    "Check code",
                    template="components/forms/prepended_appended_text.html",
                ),
                css_class="form-group col-md-4 mb-0 mt-2",
            ),
            Column(
                PrependedText(
                    "tags",
                    "Tags",
                    template="components/forms/prepended_appended_text.html",
                ),
                css_class="form-group col-md-6 mb-0 mt-2",
            ),
            Column(
                PrependedText(
                    "weight",
                    fa_icon("balance-scale", "Weight"),
                    template="components/forms/prepended_appended_text.html",
                ),
                css_class="input-group-sm col-md-2 mb-0 mt-2",
            ),
            css_class="form-row",
        ),
        Row(
            Column("description", css_class="form-group col-md-12 mb-0"),
            css_class="form-row",
        ),
        TabHolder(
            Tab(
                "Left",
                Row(
                    prepended_select_column("left_system", 3, "m-1"),
                    prepended_select_column("left_type", 3, "m-1"),
                ),
                Row(Column("left_logic", css_class="form-group col-md-12 mb-0")),
            ),
            Tab(
                "Right",
                Row(
                    prepended_select_column("relation", 2, "m-1"),
                    prepended_select_column("right_system", 3, "m-1"),
                    prepended_select_column("right_type", 3, "m-1"),
                ),
                Row(Column("right_logic", css_class="form-group col-md-12 mb-0")),
            ),
            Tab(
                "Warning",
                Row(
                    Column(
                        "supports_warning", css_class="form-group col-md-1 mb-0 mt-1"
                    ),
                    prepended_select_column("warning_relation", 2, "m-1"),
                    prepended_select_column("warning_type", 3, "m-1"),
                ),
                Row(Column("warning_logic", css_class="form-group col-md-12 mb-0")),
            ),
        ),
        Submit("submit", "Submit", css_class="btn-sm"),
    )

    class Meta:
        model = Datacheck
        fields = [
            "code",
            "description",
            "weight",
            "left_system",
            "left_type",
            "left_logic",
            "relation",
            "right_system",
            "right_type",
            "right_logic",
            "supports_warning",
            "warning_relation",
            "warning_type",
            "warning_logic",
            "tags",
        ]
        widgets = {
            "description": forms.Textarea({"cols": 40, "rows": 3}),
            "left_logic": CodeMirrorWidget(config_name="inspector"),
            "right_logic": CodeMirrorWidget(config_name="inspector"),
            "warning_logic": CodeMirrorWidget(config_name="inspector"),
        }
        system_icon = fa_icon("desktop", "System")
        labels = {
            "left_system": system_icon,
            "left_type": "Type",
            "left_logic": fa_icon("code", "Logic"),
            "right_system": system_icon,
            "right_type": "Type",
            "right_logic": fa_icon("code", "Logic"),
            "warning_type": "Type",
            "warning_relation": "Relation",
            "warning_logic": fa_icon("code", "Logic"),
            "supports_warning": "Enabled",
            "code": False,
            "weight": False,
            "tags": False,
        }


class CheckRunForm(forms.ModelForm):
    class Meta:
        model = CheckRun
        fields = [
            "start_time",
            "end_time",
            "status",
            "result",
            "left_value",
            "right_value",
            "warning_value",
            "error_message",
            "datacheck",
            "environment",
            "user",
        ]


class CheckRunFilterForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "GET"
    helper.layout = Layout(
        Row(
            prepended_select_column("datacheck", 5, "mb-1"),
            prepended_select_column("environment", 3, "mb-1"),
            prepended_select_column("status", 2, "mb-1"),
            prepended_select_column("result", 2, "mb-1"),
        ),
        Row(
            prepended_select_column("user", 3, "mb-1"),
            Column(
                Submit("submit", "Search", css_class=SUBMIT_CSS_CLASSES),
                css_class="form-group col-md-1 mb-1",
            ),
            Column(
                button_reset("checks:checkrun_list"),
                css_class="form-group col-md-1 mb-1",
            ),
            css_class="form-row",
        ),
    )

    class Meta:
        model = CheckRun
        fields = ["datacheck", "environment", "user", "status", "result"]
