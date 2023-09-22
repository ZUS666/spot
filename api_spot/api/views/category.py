from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from ..serializers import CategoriesGetSerializer
from spots.models import Category


class CategoryViewSet(RetrieveListViewSet):
    """
    Вьюсет для категорий.
    """
    queryset = Category.objects.all()
    serializer_class = CategoriesGetSerializer
    permission_classes = (AllowAny,)
