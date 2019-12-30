import django_filters

from .forms import TableProfileFilterForm
from .models import TableProfile
from ..base.constants import ICONS


class TableProfileFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["dbtable__system"].label = ICONS["system"]
        self.filters["dbtable__environment"].label = ICONS["environment"]
        self.filters["status"].label = ICONS["status"]
        self.filters["user"].label = ICONS["user"]
        self.filters["dbtable"].label = ICONS["table"]

    start_time = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = TableProfile
        fields = [
            "dbtable",
            "user",
            "status",
            "start_time",
            "dbtable__environment",
            "dbtable__system",
        ]
        form = TableProfileFilterForm
