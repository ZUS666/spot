from django.contrib import admin

from spots.models import (
    Category,
    Location,
    Price,
)
from spots.models.location import Image


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
