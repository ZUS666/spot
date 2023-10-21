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
from django.db.models import Prefetch


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
        return super().get_queryset().prefetch_related(
            Prefetch('location_extra_photo')
        )


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


class LocationBigQueryViewSet(RetrieveListViewSet):
    """
    Представление подробной информации о локациях с возможностью фильтрации
    по названию, категориям, метро и избранному.
    """
    from api.serializers.locations import LocationGetBigQuerySerializer

    queryset = Location.objects.all()
    serializer_class = LocationGetBigQuerySerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = LocationFilter
    search_fields = ('$name', )

    def get_queryset(self):
        from django.db.models import Avg, Count, Min, OuterRef, Subquery, Value
        from django.db.models.functions import Coalesce
        from spots.models import Spot
        return Location.objects.annotate(
            minprice=Subquery(
                Spot.objects.filter(location=OuterRef('id'))
                .values('location')
                .annotate(min=Min('price__total_price'))
                .values('min')
            ),
            rating_1=Coalesce(Subquery(
                Spot.objects.filter(location=OuterRef('id'))
                .values('location')
                .annotate(avg=Avg('orders__reviews__rating'))
                .values('avg')
            ), Value(0.0)),
            workspace=Coalesce(Subquery(
                Spot.objects.filter(
                    location=OuterRef('id'),
                    category='Рабочее место'
                ).values('location')
                .annotate(count=Count('pk'))
                .values('count')
            ), Value(0)),
            meetings=Coalesce(Subquery(
                Spot.objects.filter(
                    location=OuterRef('id'),
                    category='Переговорная'
                ).values('location')
                .annotate(count=Count('pk'))
                .values('count')
            ), Value(0)),
        ).prefetch_related(
            Prefetch('location_extra_photo')
        )
