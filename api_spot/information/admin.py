from django.contrib import admin

from information.models import Event, Question, Rule


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'date',
        'meeting_quantity',
        'url',
    )
    list_per_page = 15


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
    )
    list_per_page = 15


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text'
    )
    list_per_page = 15
