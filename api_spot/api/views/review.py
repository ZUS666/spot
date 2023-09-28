from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.mixins import CreateDestroyViewSet, RetrieveListViewSet
from api.serializers.review import ReviewGetSerializer, ReviewSerializer
from spots.models import Location, Review


class ReviewCreateViewSet(CreateDestroyViewSet):
    """Вьюсет модели отзывов для создания и удаления."""
    queryset = Review.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer


class ReviewGetViewSet(RetrieveListViewSet):
    """Вьюсет модели отзывов для получения."""
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
