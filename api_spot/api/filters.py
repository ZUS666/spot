import django_filters

from spots.models import Location


class LocationFilter(django_filters.FilterSet):
    """Класс FilterSet для фильтрации локации."""
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Location
        fields = ('name',)
