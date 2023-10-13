from django.contrib import admin
from django.utils.safestring import mark_safe

from spots.models import (
    Equipment, Event, ExtraPhoto, Favorite, Location, Order, PlanPhoto, Price,
    Question, Review, Rule, SmallMainPhoto, Spot, SpotEquipment,
)


@admin.register(SmallMainPhoto)
class SmallMainPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'preview')
    readonly_fields = ('preview', )

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 300px;">'
        )


@admin.register(ExtraPhoto)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'preview')

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 300px;">'
        )


class ImageInline(admin.TabularInline):
    model = ExtraPhoto
    extra = 0


class PlanPhotoInline(admin.StackedInline):
    model = PlanPhoto
    max_num = 1
    min_num = 1


class SmallMainPhotoInline(admin.StackedInline):
    model = SmallMainPhoto
    max_num = 1
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
    inlines = (ImageInline, PlanPhotoInline, SmallMainPhotoInline)


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
    exclude = ('bill',)
    empty_value_display = '-пусто)))-'


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )


@admin.register(Event)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'date',
        'meeting_quantity',
        'url',
    )


@admin.register(Question)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
    )


@admin.register(Rule)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
    )
