from django.conf import settings
from django.core.cache import cache
from django.db.models import Avg, Min

from spots.constants import NAME_CACHE_LOW_PRICE, NAME_CACHE_RATING


def count_spots(self, category, name_cache):
    """
    Получение количества мест по категории в локации.
    """
    count = cache.get(f'{self.id}{name_cache}')
    if count is None:
        count = self.spots.filter(category=category).count()
        cache.set(
            f'{self.id} {name_cache}',
            count,
            settings.TIMEOUT_CACHED_COUNTER
        )
    return count


def get_rating_location(self):
    """
    Получение рейтинга по отзывам для локации.
    Кеш не инвалидируется.
    """
    from .models import Review
    rating = cache.get(f'{self.id}{NAME_CACHE_RATING}')
    if rating is None:
        rating = Review.objects.filter(
            booked_spot_id__spot_id__location_id=self.id).aggregate(
                Avg('rating')).get('rating__avg')
        cache.set(f'{self.id}{NAME_CACHE_RATING}',
                  rating,
                  settings.TIMEOUT_CACHED_RATING
                  )
    return rating


def get_low_price(self):
    """
    Получение самой низкой цены локации.
    Кеш не инвалидируется.
    """
    low_price = cache.get(f'{self.id}{NAME_CACHE_LOW_PRICE}')
    if low_price is None:
        low_price = self.spots.aggregate(
            Min('price__total_price')).get('price__total_price__min')
        cache.set(f'{self.id}{NAME_CACHE_LOW_PRICE}',
                  low_price,
                  settings.TIMEOUT_CACHED_LOW_PRICE)
    return low_price
