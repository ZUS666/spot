from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from api.serializers import (
    SpotDetailSerializer, SpotQuerySerializer, SpotSerializer,
)
from spots.models import Location, Spot
from spots.validators import check_date_time


@extend_schema(
    tags=('spots',),
    parameters=[
        OpenApiParameter(
            name='date', location='query', required=True,
            description='Дата в формате YYYYY-MM-DD',
        ),
        OpenApiParameter(
            name='start_time', location='query', required=True,
            description='Время в формате HH:MM',
        ),
        OpenApiParameter(
            name='end_time', location='query', required=True,
            description='Время в формате HH:MM',
        ),
    ]
)
class SpotViewSet(RetrieveListViewSet):
    """
    Представление для мест в локациях с возможностью фильтрации
    по категериям.
    """
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpotDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        location_id = self.kwargs.get('location_id')
        return super().get_queryset().filter(
            location_id=location_id).select_related('price')
    
    def get_serializer_context(self):
        """
        Добавление в контекс query_params и их валидация через сериализатор.
        """
        context = super().get_serializer_context()
        if self.action == 'retrieve':
            return context
        query = SpotQuerySerializer(data=self.request.query_params)
        query.is_valid(raise_exception=True)
        location_id = self.kwargs.get('location_id')
        date = query.validated_data.get('date')
        start_time = query.validated_data.get('start_time')
        end_time = query.validated_data.get('end_time')
        location = get_object_or_404(Location, id=location_id)
        check_date_time(
            date,
            start_time,
            end_time,
            location,
            DRFValidationError,
        )
        context['date'] = date
        context['start_time'] = start_time
        context['end_time'] = end_time
        return context
