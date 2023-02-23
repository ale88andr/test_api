from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models.users import User


####################
# Models
####################
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'email', )}),
        (_('Личная информация'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'full_name', 'username', 'phone_number', 'email', )
    list_display_links = ('id', 'email', 'full_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups',)
    search_fields = ('first_name', 'last_name', 'id', 'email', 'phone_number',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions', )
    readonly_fields = ('last_login',)
