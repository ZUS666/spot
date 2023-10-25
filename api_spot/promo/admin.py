from django.contrib import admin
from promo.models import EmailNews, Promocode


@admin.register(Promocode)
class PromcodeAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailNews)
class EmailNewsAdmin(admin.ModelAdmin):
    pass
