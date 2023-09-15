from django.contrib import admin

from spots.models.review import Review
from spots.models.order import Order
from spots.models.spot import Spot


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name"
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booked_spot",
        "pub_date",
    )
    readonly_fields = ('pub_date',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "spot",
        "user",
        "start_date",
        "end_date"
    )
    empty_value_display = "-пусто)))-"
