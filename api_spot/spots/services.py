from django.conf import settings
from django.core.cache import cache


def count_spots(self, category, name_cache):
    count = cache.get(f'{self.id} {name_cache}')
    if count is None:
        count = self.spots.filter(category=category).count()
        cache.set(
            f'{self.id} {name_cache}',
            count,
            settings.TIMEOUT_CACHED_COUNTER
        )
    return count
