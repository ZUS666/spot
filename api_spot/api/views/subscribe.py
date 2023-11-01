from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.constants import SUBJECT_EMAIL_SUBSCRIPTION, SUBSCRIPTION_TEMPLATE
from api.exceptions import NotSubscribedUserError, SubscribedUserError
from api.services.subscribe import subscribe_service
from api.tasks import send_mail_task


@extend_schema(
    tags=('subscribe',)
)
class SubscireAPIView(APIView):
    """
    Представление подписки и отписки на новостную рассылку.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        subscribe_service(user, SubscribedUserError, True)
        send_mail_task.delay(
            user.email,
            SUBJECT_EMAIL_SUBSCRIPTION,
            SUBSCRIPTION_TEMPLATE,
        )
        return Response(
            {'message': 'Вы успешно подписались'}, status=status.HTTP_200_OK
        )

    def delete(self, request):
        user = self.request.user
        subscribe_service(user, NotSubscribedUserError, False)
        return Response(
            {'message': 'Вы успешно отписались'}, status=status.HTTP_200_OK
        )
