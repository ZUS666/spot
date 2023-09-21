from django.shortcuts import get_object_or_404

from api.mixins import CreateDestroyViewSet, RetrieveListViewSet
from api.serializers.review import ReviewSerializer
from spots.models import Review, Spot


class ReviewCreateViewSet(CreateDestroyViewSet):
    """Вьюсет модели отзывов для создания и удаления."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewGetViewSet(RetrieveListViewSet):
    """Вьюсет модели отзывов для получения."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Получение выборки с отзывами текущего спота."""
        if self.kwargs.get('spot_id') is not None:
            spot = get_object_or_404(Spot, pk=self.kwargs.get('spot_id'))
            return super().get_queryset().filter(booked_spot__spot=spot)
