from rest_framework import viewsets

from api.permissions import IsOwnerOrReadOnly
from api.serializers.avatar import AvatarSerializer
from users.models import Avatar


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )
