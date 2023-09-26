from django.db.models import Q


def is_ordered_spot(instance, date, start_time, end_time):
    """
    Получение информации о наличии бронирований в заданный
    промежуток даты и времени.
    """
    return instance.orders.filter(
        Q(
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        ) | Q(
            date=date,
            start_time__lt=start_time,
            end_time__gt=end_time)).exists()
