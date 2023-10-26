from django.contrib import admin

from promo.models import EmailNews, Promocode


@admin.register(Promocode)
class PromcodeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'percent_discount',
        'expiry_date',
        'balance',
    )


@admin.register(EmailNews)
class EmailNewsAdmin(admin.ModelAdmin):
    list_display = (
        'subject_message',
        'send_date',
        'promocode',
        'is_sent',
        'text_message',
    )
    exclude = ('is_sent',)
