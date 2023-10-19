from django_filters import rest_framework as filters

from spots.constants import CANCEL, CATEGORY_CHOICES, FINISH
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
        return queryset.exclude(status__in=[FINISH, CANCEL])

    class Meta:
        model = Order
        fields = (
            'finished',
        )


class LocationFilter(filters.FilterSet):
    """
    Фильтрация локаций по названию, метро, категориям спотов и избранному.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['metro'].extra['choices'] = self.get_metro_choices()

    def get_metro_choices(self):
        metro_list = Location.objects.values_list(
            'metro', flat=True
        ).distinct()
        return [(metro, metro) for metro in metro_list]

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )
    metro = filters.MultipleChoiceFilter(
        choices=[]
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
