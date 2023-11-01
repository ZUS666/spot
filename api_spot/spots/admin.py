from django.contrib import admin
from django.utils.safestring import mark_safe

from spots.models import (
    Equipment, ExtraPhoto, Favorite, Location, Order, PlanPhoto, Price, Review,
    SmallMainPhoto, Spot, SpotEquipment,
)


@admin.register(SmallMainPhoto)
class SmallMainPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'preview')
    readonly_fields = ('preview', )
    list_per_page = 5

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 300px;">'
        )


@admin.register(PlanPhoto)
class PlanPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'preview')
    readonly_fields = ('preview', )
    list_per_page = 5

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 300px;">'
        )


@admin.register(ExtraPhoto)
class ExtraPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'preview')
    list_per_page = 10

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
    list_filter = ('street', 'metro', 'city',)
    inlines = (ImageInline, PlanPhotoInline, SmallMainPhotoInline)
    list_per_page = 10


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('price', 'discount', 'total_price', 'description')
    exclude = ('total_price',)
    list_filter = ('spots__location',)
    search_fields = ('spot', )
    list_per_page = 10


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location')
    list_per_page = 10


class SpotEquipmentInline(admin.TabularInline):
    model = SpotEquipment
    extra = 0
    min_num = 1


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'location', 'category', 'price')
    list_filter = ('location', 'category',)
    inlines = (SpotEquipmentInline,)
    list_per_page = 15


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'booked_spot',
        'pub_date',
    )
    list_filter = ('booked_spot__spot__location',)
    search_fields = ('pub_date',)
    search_help_text = 'Поиск по дате публикации в формате гггг-мм-дд'
    readonly_fields = ('pub_date',)
    list_per_page = 15


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'spot', 'user', 'date',
        'start_time', 'end_time', 'status',
        'bill'
    )
    readonly_fields = ('bill',)
    list_filter = ('spot__location', 'date',)
    search_fields = ('date',)
    search_help_text = 'Поиск по дате в формате гггг-мм-дд'
    list_per_page = 15


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )
    list_per_page = 15
