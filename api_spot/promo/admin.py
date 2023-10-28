from django.contrib import admin

from promo.models import EmailNews, Promocode


@admin.register(Promocode)
class PromcodeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'percent_discount',
        'expiry_date',
        'balance',
    )


@admin.register(EmailNews)
class EmailNewsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'subject_message',
        'send_datetime',
        'promocode',
        'is_sent',
        'text_message',
    )
    exclude = ('is_sent',)
    readonly_fields = ('task',)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.task:
                obj.task.delete()
        return super().delete_queryset(request, queryset)
