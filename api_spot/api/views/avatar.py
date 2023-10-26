from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response

from api.mixins import CreateUpdateDeleteViewSet
from api.permissions import IsOwnerOrReadOnly
from api.serializers.avatar import AvatarSerializer
from users.models import Avatar


@extend_schema(
    tags=('avatar',)
)
class AvatarViewSet(CreateUpdateDeleteViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )

    def update(self, request,):
        print(request.user)
        instance = get_object_or_404(
            Avatar,
            user=request.user,
        )
        serializer = self.get_serializer(
            instance, data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def delete(self, request,):
        """Удаление аватарки."""
        avatar = get_object_or_404(
            Avatar,
            user=request.user,
        )
        avatar.delete()
        return Response(
            {'message': 'Аватрка удалена'},
            status=status.HTTP_200_OK
        )
