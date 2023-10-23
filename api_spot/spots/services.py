from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from PIL import Image

from spots.constants import NAME_CACHE_MEETING_ROOM, NAME_CACHE_WORKSPACE


def count_spots(location, category, name_cache):
    """
    Получение количества мест по категории в локации.
    """
    count = cache.get(f'{location.id}{name_cache}')
    if count is None:
        count = location.spots.filter(category=category).count()
        cache.set(
            f'{location.id}{name_cache}',
            count,
            settings.TIMEOUT_CACHED_COUNTER
        )
    return count


def delete_location_cache_in_spot(location_id):
    cache.delete(f'{location_id}{NAME_CACHE_WORKSPACE}')
    cache.delete(f'{location_id}{NAME_CACHE_MEETING_ROOM}')


def image_resize(image, width, height):
    image_types = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "gif": "GIF",
        "tif": "TIFF",
        "tiff": "TIFF",
    }
    img = Image.open(image)
    if img.width > width or img.height > height:
        img.thumbnail((width, height))
        img_filename = Path(image.file.name).name
        img_suffix = Path(image.file.name).name.split(".")[-1]
        img_format = image_types[img_suffix]
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        file_object = ContentFile(buffer.getvalue())
        image.save(img_filename, file_object)
