def subscribe_service(self, error, bool):
    user = self.request.user
    if user.is_subscribed is bool:
        raise error
    user.is_subscribed = bool
    user.save(update_fields=['is_subscribed'])
