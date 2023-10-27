from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import NotSubscribedUserError, SubscribedUserError
from api.services.subscribe import subscribe_service

User = get_user_model()


@extend_schema(
    tags=('subscribe',)
)
class SubscireAPIView(APIView):
    """
    Представление подписки и отписки на новостную рассылку.
    """
    permission_classes = (IsAuthenticated,)

    def post(self):
        subscribe_service(self, SubscribedUserError, True)
        return Response(
            {'message': 'Вы успешно подписались'}, status=status.HTTP_200_OK
        )

    def delete(self):
        subscribe_service(self, NotSubscribedUserError, False)
        return Response(
            {'message': 'Вы успешно отписались'}, status=status.HTTP_200_OK
        )
