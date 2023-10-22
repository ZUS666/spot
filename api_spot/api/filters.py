from django_filters import rest_framework as filters

from spots.constants import CANCEL, CATEGORY_CHOICES, FINISH, NOT_PAID
from spots.models import Location, Order, SpotEquipment


class OrderFilter(filters.FilterSet):
    """Класс FilterSet для фильтрации заказа."""
    finished = filters.BooleanFilter(
        method='filter_finished',
        label='finished',
    )

    def filter_finished(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(status__in=[FINISH, CANCEL])
        return queryset.exclude(status__in=[FINISH, CANCEL, NOT_PAID])

    class Meta:
        model = Order
        fields = (
            'finished',
        )


class LocationFilter(filters.FilterSet):
    """
    Фильтрация локаций по названию, метро, категориям спотов и избранному.
    """
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )
    metro = filters.MultipleChoiceFilter(
        choices=[
            (i, i) for i in Location.objects.values_list(
                'metro', flat=True).distinct()
        ],
        field_name='metro',
    )
    city = filters.CharFilter(
        field_name='city',
        lookup_expr='istartswith',
    )
    category = filters.ChoiceFilter(
        distinct=True,
        field_name='spots__category',
        choices=CATEGORY_CHOICES,
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    class Meta:
        model = Location
        fields = (
            'name',
            'metro',
            'city',
            'category',
            'is_favorited',
        )


class SpotEquipmentFilter(filters.FilterSet):
    """Класс FilterSet для фильтрации обородувания."""
    category = filters.ChoiceFilter(
        choices=CATEGORY_CHOICES,
        field_name='spot__category',
    )

    class Meta:
        model = SpotEquipment
        fields = (
            'category',
        )
