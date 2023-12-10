from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.mixins import CreateDestroyViewSet
from api.serializers import (
    UserAvatarInputSerializer, UserAvatarOutputSerializer,
)
from users.models import Avatar


@extend_schema(
    tags=('avatar',)
)
class UserAvatarViewSet(CreateDestroyViewSet):
    """
    Представление добавления/изменения и удаления аватара пользователя.
    """
    queryset = Avatar.objects.all()
    serializer_class = UserAvatarInputSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        avatar, _ = Avatar.objects.update_or_create(serializer.validated_data)
        serializer = UserAvatarOutputSerializer(
            avatar,
            context=self.get_serializer_context()
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request) -> Response:
        obj = get_object_or_404(Avatar, user=request.user)
        obj.delete()
        return Response(
            {'message': 'Изображение успешно удалено'},
            status=status.HTTP_200_OK
        )
