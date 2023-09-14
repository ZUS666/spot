from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets

from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.users import (UserMeSerializer, UserSerializer,
                                 SendConfirmationCodeSerializer,
                                 ActivationUserSerializer)
from ..services.users import (cache_and_send_confirmation_code,
                              finish_activation_email)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def get_permissions(self):
        if self.action in ('create', 'activation'):
            return (AllowAny(),)
        return super().get_permissions()

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        cache_and_send_confirmation_code(user)

    @action(
        detail=False,
        methods=['post'],
        # permission_classes=(AllowAny(),),
        serializer_class=ActivationUserSerializer
    )
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        if confirmation_code == cache.get(user.id):
            user.is_active = True
            user.save()
            finish_activation_email(user.email)
            return Response(
                {'message': 'Электронная почта верифицирована'},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            {'message': 'Не действительный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer
    )
    def me(self, request):
        """
        Любой пользователь может получить информацию о себе.
        """
        email = request.user.email
        user = User.objects.get(email=email)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def patch_me(self, request, *args, **kwargs):
        """
        Любой пользователь может изменить информацию о себе.
        """
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SendCodeAPIView(APIView):
    """
    Отправляет код активации
    """

    def post(self, request):
        serializer = SendConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        cache_and_send_confirmation_code(user)
        return Response(
            {'message': 'Код активации отправлен на почту'}
        )
