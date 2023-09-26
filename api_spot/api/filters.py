import django_filters

from spots.models import Order, Location, SpotEquipment
from spots.constants import FINISH, CATEGORY_CHOICES


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
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
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
            'favorite', 'name',
        )


class SpotEquipmentFilter(django_filters.FilterSet):
    """Класс FilterSet для фильтрации обородувания."""
    category = django_filters.ChoiceFilter(
        choices=CATEGORY_CHOICES,
        field_name='spot__category',
    )

    class Meta:
        model = SpotEquipment
        fields = (
            'category',
        )
