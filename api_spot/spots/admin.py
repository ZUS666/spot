from django.contrib import admin

from .models import (Equipment, ExtraPhoto, Favorite, Location, Order, Price,
                     Review, Spot, SpotEquipment)


@admin.register(ExtraPhoto)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('location', 'id', 'image', 'description')


class ImageInline(admin.TabularInline):
    model = ExtraPhoto
    extra = 0
    min_num = 1


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'street',
        'house_number',
        'open_time',
        'close_time',
        'latitude',
        'longitude',
    )
    list_filter = ('street', 'house_number')
    search_fields = ('street', 'house_number')
    inlines = [ImageInline]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('price', 'discount', 'total_price', 'description')
    exclude = ('total_price',)
    search_fields = ('spot', )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location')


class SpotEquipmentInline(admin.TabularInline):
    model = SpotEquipment
    extra = 0
    min_num = 1


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'location', 'category', 'price')
    list_filter = ('location', 'category',)
    inlines = (SpotEquipmentInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'booked_spot',
        'pub_date',
    )
    readonly_fields = ('pub_date',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'spot', 'user', 'date',
        'start_time', 'end_time', 'status'
    )
    empty_value_display = '-пусто)))-'


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'description')
