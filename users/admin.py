from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    ordering = ('email',)

    fieldsets = UserAdmin.fieldsets + (
        ('Роль пользователя', {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Роль пользователя', {'fields': ('role',)}),
    )
