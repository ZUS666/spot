import os
import uuid

from django.db.models import Model


def get_avatar_path(instance: Model, filename: str) -> str:
    """Загрузка с уникальным именем."""
    ext: str = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('images/users', filename)
