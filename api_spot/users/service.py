import os
import uuid

from users.models import Avatar


def get_avatar_path(instance: Avatar, filename: str) -> str:
    """Загрузка с уникальным именем."""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('images/users', filename)
