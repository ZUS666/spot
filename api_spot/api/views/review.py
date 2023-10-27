from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.mixins import CreateDestroyViewSet, RetrieveListViewSet
from api.serializers.review import ReviewGetSerializer, ReviewSerializer
from spots.models import Location, Review


@extend_schema(
    tags=('reviews',)
)
class ReviewCreateViewSet(CreateDestroyViewSet):
    """
    Представление для создания и удаления отзывов к локациям
    по завершенным заказам.
    """
    queryset = Review.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def destroy(self, request, *args, **kwargs):
        """Удаление отзыва."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Отзыв успешно удален'},
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=('reviews',)
)
class ReviewGetViewSet(RetrieveListViewSet):
    """
    Представление для вывода отзывов по локациям.
    """
    queryset = Review.objects.select_related(
        'booked_spot__user', 'booked_spot__user__avatar'
    ).all()
    serializer_class = ReviewGetSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Получение выборки с отзывами текущей локации."""
        if self.kwargs.get('location_id') is not None:
            location = get_object_or_404(
                Location, pk=self.kwargs.get('location_id')
            )
            return super().get_queryset().filter(
                booked_spot__spot__location=location
            )
