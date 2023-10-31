from django.db.models.signals import post_delete
from django.dispatch import receiver

from spots.models import Spot
from spots.services import delete_location_cache_in_spot


@receiver(post_delete, sender=Spot)
def delete_cache_spots_signal(sender, instance, *args, **kwargs):
    delete_location_cache_in_spot(instance.location.id)
