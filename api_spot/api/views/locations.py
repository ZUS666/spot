from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from api.filters import LocationFilter
from api.mixins import RetrieveListViewSet
from api.serializers import (
    LocationGetSerializer, LocationGetShortSerializer, LocationMapSerializer,
)
from spots.models import Location


class LocationViewSet(RetrieveListViewSet):
    """
    Представление подробной информации о локациях с возможностью фильтрации
    по названию, категориям, метро и избранному.
    """
    queryset = Location.objects.all()
    serializer_class = LocationGetSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = LocationFilter
    search_fields = ('$name', )

    def get_queryset(self):
        from django.db.models import Avg, Q, Count, Min, OuterRef, Prefetch, Subquery
        from spots.models import Favorite
        user_id = self.request.user
        qs = Location.objects.annotate(
            is_favorited=Subquery(
                Favorite.objects.filter(
                    location=OuterRef('id'),
                    user=user_id
                ).values('user')
            ),
            minprice=Min('spots__price__total_price'),
            rating_1=Avg('spots__orders__reviews__rating'),
            workspace=Count('spots', filter=Q(spots__category='Рабочее место')),
            meetings=Count('spots', filter=Q(spots__category='Переговорная')),
        ).prefetch_related(
            Prefetch('location_extra_photo')
        )

        return qs

@extend_schema(
    tags=('locations',)
)
class LocationShortListAPIView(ListAPIView):
    """
    Представление краткой информации о локациях с возможностью фильтрации
    по названию, категориям, метро и избранному и поиску по названию.
    """
    queryset = Location.objects.all()
    serializer_class = LocationGetShortSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = LocationFilter
    search_fields = ('$name', )


@extend_schema(
    tags=('locations',)
)
class LocationMapListAPIView(ListAPIView):
    """
    Представление краткой информации о локациях для отображения на карте.
    """
    queryset = Location.objects.all().prefetch_related('small_main_photo')
    serializer_class = LocationMapSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LocationFilter
