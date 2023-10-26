from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.mixins import UpdateDeleteViewSet
from api.serializers.avatar import AvatarSerializer
from users.models import Avatar


@extend_schema(
    tags=('avatar',)
)
class AvatarViewSet(UpdateDeleteViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request,):
        instance, _ = Avatar.objects.get_or_create(user=request.user,)
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
        avatar.image = ''
        avatar.save()
        return Response(
            {'message': 'Аватрка удалена'},
            status=status.HTTP_200_OK
        )
