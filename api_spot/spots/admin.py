from django.contrib import admin

from spots.models import (
    Category,
    Location,
    Price,
)
from spots.models.location import Image
from spots.models.favorite import Favorite
from spots.models.location import Location
from spots.models.order import Order
from spots.models.review import Review
from spots.models.spot import Spot


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image', 'description')


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    min_num = 1


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'street',
        'house_number',
        'apartment_number',
        'latitude',
        'longitude',
    )
    list_filter = ('street', 'house_number')
    search_fields = ('street', 'house_number')
    exclude = ('images',)
    inlines = [ImageInline]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('price', 'discount', 'description')
    # search_fields = ('spot', )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "location"
    )

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

