from django.db.models import Avg, Count, Min, Prefetch
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
        user = self.request.user
        if user.is_authenticated:
            qs = super().get_queryset().annotate(
                is_favorited=Count('favorites', favorites__user=user),
                low_price=Min('spots__price__total_price'),
                rating=Avg('spots__orders__reviews__rating'),
            ).prefetch_related(
                Prefetch('location_extra_photo')
            )
        else:
            qs = super().get_queryset().annotate(
                low_price=Min('spots__price__total_price'),
                rating=Avg('spots__orders__reviews__rating'),
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

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return super().get_queryset().annotate(
                is_favorited=Count('favorites', favorites__user=user),
                low_price=Min('spots__price__total_price'),
                rating=Avg('spots__orders__reviews__rating')
            )
        return super().get_queryset().annotate(
            low_price=Min('spots__price__total_price'),
            rating=Avg('spots__orders__reviews__rating'),
        )


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

    def get_queryset(self):
        return super().get_queryset().annotate(
            rating=Avg('spots__orders__reviews__rating')
        )
