import uuid
import os


def get_avatar_path(instance, filename):
    """Загрузка с уникальным именем."""
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/users', filename)
