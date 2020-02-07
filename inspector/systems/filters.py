import django_filters

from .forms import DbTableFilterForm
from .models import DbTable
from ..base.constants import ICONS


class DbTableFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["system"].label = ICONS["system"]
        self.filters["environment"].label = ICONS["environment"]
        self.filters["schema"].label = ICONS["schema"]

    schema = django_filters.ModelChoiceFilter(
        queryset=DbTable.objects.values_list("schema", flat=True)
        .distinct()
        .order_by("schema")
    )

    class Meta:
        model = DbTable
        fields = [
            "system",
            "environment",
        ]
        form = DbTableFilterForm
