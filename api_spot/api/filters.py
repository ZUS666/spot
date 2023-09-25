import django_filters

from spots.models import Order, Location
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


class LocationFilter(django_filters.FilterSet):
    """Класс FilterSet для фильтрации локации."""
    favorite = django_filters.NumberFilter(
        method='filter_favorite', label='favorite'
    )

    def filter_favorite(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value == 1:
                return queryset.filter(
                    favorites__user=self.request.user
                )
            if value == 0:
                return queryset.exclude(
                    favorites__user=self.request.user
                )
        return queryset

    class Meta:
        model = Location
        fields = (
            'favorite',
        )
