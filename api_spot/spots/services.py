from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.db.models import Avg, Min
from PIL import Image

from spots.constants import (
    NAME_CACHE_LOW_PRICE, NAME_CACHE_MEETING_ROOM, NAME_CACHE_RATING,
    NAME_CACHE_WORKSPACE,
)


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


def get_rating_location(location):
    """
    Получение рейтинга по отзывам для локации.
    Кеш не инвалидируется.
    """
    from .models import Review
    rating = cache.get(f'{location.id}{NAME_CACHE_RATING}')
    if rating is None:
        rating = Review.objects.filter(
            booked_spot_id__spot_id__location_id=location.id).aggregate(
                Avg('rating')).get('rating__avg')
        cache.set(f'{location.id}{NAME_CACHE_RATING}',
                  rating,
                  settings.TIMEOUT_CACHED_RATING
                  )
    if rating:
        rating = round(rating, 1)
    return rating


def get_low_price(location):
    """
    Получение самой низкой цены локации.
    Кеш не инвалидируется.
    """
    low_price = cache.get(f'{location.id}{NAME_CACHE_LOW_PRICE}')
    if low_price is None:
        low_price = location.spots.aggregate(
            Min('price__total_price')).get('price__total_price__min')
        cache.set(f'{location.id}{NAME_CACHE_LOW_PRICE}',
                  low_price,
                  settings.TIMEOUT_CACHED_LOW_PRICE)
    return low_price


def delete_location_cache_in_spot(location_id):
    cache.delete(f'{location_id}{NAME_CACHE_WORKSPACE}')
    cache.delete(f'{location_id}{NAME_CACHE_MEETING_ROOM}')
    cache.delete(f'{location_id}{NAME_CACHE_LOW_PRICE}')


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
