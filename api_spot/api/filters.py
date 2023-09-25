import django_filters

from spots.models import Order
from spots.constants import FINISH


class OrderFilter(django_filters.FilterSet):
    """Класс FilterSet для фильтрации заказа."""
    finished = django_filters.NumberFilter(
        method='filter_finished', label='finished'
    )

    def filter_finished(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value == 1:
                return queryset.filter(
                    status=FINISH
                )
            if value == 0:
                return queryset.exclude(
                    status=FINISH
                )
        return queryset

    class Meta:
        model = Order
        fields = (
            'finished',
        )
