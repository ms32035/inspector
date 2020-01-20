import django_filters

from .forms import CheckRunFilterForm
from .models import CheckRun
from ..base.constants import ICONS


class CheckRunFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["environment"].label = ICONS["environment"]
        self.filters["datacheck"].label = ICONS["datacheck"]
        self.filters["status"].label = ICONS["status"]
        self.filters["user"].label = ICONS["user"]
        self.filters["result"].label = ICONS["result"]

    start_time = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = CheckRun
        fields = ["environment", "datacheck", "user", "status", "result", "start_time"]
        form = CheckRunFilterForm
