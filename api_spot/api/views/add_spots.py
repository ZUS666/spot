from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiExample, OpenApiResponse, extend_schema,
)
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.exceptions import AddSpotsError
from api.serializers import AddSpotsSerializer
from spots.models import Location, Spot, SpotEquipment


@extend_schema(
    responses=OpenApiResponse(
        {201: None},
        examples=[OpenApiExample(
            name='example', value={'count_created_spots': '5'}
        )]
    )
)
class AddSpotsAPIView(CreateAPIView):
    """
    Представление для массового создания мест администратором.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = AddSpotsSerializer

    @transaction.atomic
    def post(self, request, location_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        get_object_or_404(Location, id=location_id)
        names = serializer.validated_data.get('names')
        price = serializer.validated_data.get('price_id')
        category = serializer.validated_data.get('category')
        description = serializer.validated_data.get('description')
        equipments = serializer.validated_data.get('equipments_id')
        list_names = names.replace(' ', '').split(',')
        bulk = [Spot(
            name=name,
            price=price,
            location_id=location_id,
            category=category,
            description=description) for name in list_names]
        try:
            new_spots = Spot.objects.bulk_create(bulk)
        except IntegrityError:
            raise AddSpotsError
        bulk2 = [
            SpotEquipment(
                spot=sp,
                equipment=eq
            ) for sp in new_spots for eq in equipments
        ]
        SpotEquipment.objects.bulk_create(bulk2)
        return Response(
            {'count_created_spots': len(new_spots)},
            status=status.HTTP_201_CREATED
        )
