from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.generics import RetrieveAPIView

from api.serializers import PlanPhotoGetSerializer
from spots.models import PlanPhoto


@extend_schema(
    tags=('locations',)
)
class PlanPhotoAPIView(RetrieveAPIView):
    """
    Представление для вывода фотографии плана локации.
    """
    permission_classes = (AllowAny,)

    def get_object(self, location_id):
        return get_object_or_404(PlanPhoto, location_id=location_id)

    def get(self, request, location_id, *args, **kwargs):
        serializer = PlanPhotoGetSerializer(
            self.get_object(location_id),
            context=self.get_serializer_context()
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
