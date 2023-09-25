from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from ..serializers import (SpotDetailSerializer, SpotSerializer,
                           SpotQuerySerializer)
from spots.models import Spot


class SpotViewSet(RetrieveListViewSet):
    """
    Вьюсет для локаций.
    """
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpotDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        location_id = self.kwargs.get('location_id')
        return super().get_queryset().filter(location_id=location_id)

    def get_serializer_context(self):
        """
        Добавление в контекс query_params и их валидация через сериализатор.
        """
        context = super().get_serializer_context()
        if self.action == 'retrieve':
            return context
        query = SpotQuerySerializer(data=self.request.query_params)
        query.is_valid(raise_exception=True)
        context['date'] = query.validated_data.get('date')
        context['start_time'] = query.validated_data.get('start_time')
        context['end_time'] = query.validated_data.get('end_time')
        return context
