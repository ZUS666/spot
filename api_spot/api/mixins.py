from rest_framework import mixins, viewsets


class RetrieveListCreateDestroyViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Класс ViewSet только для получения, создания и удаления объектов."""
    pass


class RetrieveListViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Класс ViewSet только для получения объектов(-а)."""
    pass


class CreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Класс ViewSet только для создания и удаления объектов(-а)."""
    pass


class CreateUpdateViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """Класс ViewSet только для создания и изменения объектов(-а)."""
    pass
