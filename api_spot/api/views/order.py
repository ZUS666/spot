from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import CreateListDestroyViewSet, CreateDestroyViewSet
from api.serializers import (
    ReviewSerializer, FavoriteSerializer, ReservationSerializer)
from coworkers.models import Coworking, Favorite, Reservation
from api.permissions import IsReadOnly


class ReviewViewSet(CreateListDestroyViewSet):
    """Вьюсет модели отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = PageNumberPagination
    # фильтр по дате , надо кастомный
    filterset_fields = ("pub_date", "raitings")
    search_fields = ("text", "author__first_name")
    ordering_fields = ("pub_date", "raitings")
    ordering = ("pub_date",)

    def get_coworking(self):
        """Получение текущего объекта (коворкинга)."""
        return get_object_or_404(Coworking, pk=self.kwargs.get('coworking_id'))

    def get_queryset(self):
        """Получение выборки с отзывами текущего коворкинга."""
        return self.get_coworking().reviews.all()

    def perform_create(self, serializer):
        """Создание отзыва для текущего коворкинга."""
        serializer.save(
            author=self.request.user,
            coworking=self.get_coworking()
        )


class FavoriteViewSet(CreateDestroyViewSet):
    """Вьюсет для избранного."""
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_coworking(self):
        return get_object_or_404(Coworking, pk=self.kwargs.get('coworking_id'))

    def get_queryset(self):
        return self.request.user.favorites.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            coworking=self.get_coworking()
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['coworking_id'] = self.kwargs.get('coworking_id')
        return context

    def delete(self, request, coworking_id):
        """Отписаться от автора."""
        favorite = get_object_or_404(
            Favorite,
            user=request.user,
            coworking=get_object_or_404(Coworking, id=coworking_id),
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = PageNumberPagination
    ordering = ("start_date",)

    def get_coworking(self):
        """Получение текущего объекта (коворкинга)."""
        return get_object_or_404(Coworking, pk=self.kwargs.get('coworking_id'))

    def get_queryset(self):
        """Получение выборки с бронями текущего коворкинга."""
        return self.get_coworking().reservation.all()

    def perform_create(self, serializer):
        """Создание брони для текущего коворкинга."""
        serializer.save(
            user=self.request.user,
            coworking=self.get_coworking()
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['coworking_id'] = self.kwargs.get('coworking_id')
        return context

    def delete(self, request, coworking_id):
        """Отмена брони."""
        reservation = get_object_or_404(
            Reservation,
            user=request.user,
            coworking=get_object_or_404(Coworking, id=coworking_id),
        )
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
