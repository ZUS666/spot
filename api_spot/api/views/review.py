from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

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


@extend_schema(
    tags=('reviews',)
)
class ReviewGetViewSet(RetrieveListViewSet):
    """
    Представление для вывода отзывов по локациям.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewGetSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Получение выборки с отзывами текущей локации."""
        if self.kwargs.get('location_id') is not None:
            location = get_object_or_404(
                Location, pk=self.kwargs.get('location_id')
            )
            return super().get_queryset().filter(
                booked_spot__spot__location=location
            )
