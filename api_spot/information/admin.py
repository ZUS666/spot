from django.contrib import admin

from information.models import Event, Question, Rule


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
