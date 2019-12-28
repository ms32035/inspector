import django_filters

from .forms import TableProfileFilterForm
from ..base.constants import ICONS
from .models import TableProfile


class TableProfileFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["environment"].label = ICONS["environment"]
        self.filters["system"].label = ICONS["system"]
        self.filters["status"].label = ICONS["status"]
        self.filters["user"].label = ICONS["user"]
        self.filters["dbtable"].label = ICONS["table"]

    start_time = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = TableProfile
        fields = ["environment", "system", "dbtable", "user", "status", "start_time"]
        form = TableProfileFilterForm
