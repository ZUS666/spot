from django.apps import AppConfig


class SpotsConfig(AppConfig):
    name = 'spots'

    def ready(self) -> None:
        from spots import siglnals  # noqa: F401
