from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

from api.mixins import CreateDestroyViewSet, RetrieveListViewSet
from api.serializers.review import ReviewSerializer, ReviewGetSerializer
from spots.models import Review, Location


class ReviewCreateViewSet(CreateDestroyViewSet):
    """Вьюсет модели отзывов для создания и удаления."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewGetViewSet(RetrieveListViewSet):
    """Вьюсет модели отзывов для получения."""
    queryset = Review.objects.all()
    serializer_class = ReviewGetSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """Получение выборки с отзывами текущей локации."""
        if self.kwargs.get('location_id') is not None:
            location = get_object_or_404(
                Location, pk=self.kwargs.get('location_id')
            )
            return super().get_queryset().filter(
                booked_spot__spot__location=location
            )
