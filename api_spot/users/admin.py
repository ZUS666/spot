from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext_lazy as _

from users.models import Avatar


User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'phone',
                     'birth_date', 'occupation', 'is_subscribed')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    list_display = (
        'id', 'email', 'first_name', 'last_name',
        'phone', 'birth_date', 'occupation',
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'groups', 'is_subscribed'
    )
    search_fields = (
        'phone', 'first_name', 'last_name',
        'email', 'birth_date', 'occupation',
    )
    ordering = ('last_name', 'first_name')
    list_per_page = 15
    list_max_show_all = 30


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'preview')
    readonly_fields = ('preview', )
    list_per_page = 15
    list_max_show_all = 30

    def preview(self, obj: Avatar) -> SafeString:
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 300px;">'
            )
        return ''
