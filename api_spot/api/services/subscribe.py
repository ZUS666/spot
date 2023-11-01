def subscribe_service(user, error, bool):
    if user.is_subscribed is bool:
        raise error
    user.is_subscribed = bool
    user.save(update_fields=['is_subscribed'])
