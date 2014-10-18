from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


from .models import Player
from .forms import PlayerCreationForm, PlayerChangeForm
# Register your models here.


@admin.register(Player)
class PlayerAdmin(UserAdmin):

    form = PlayerChangeForm
    add_form = PlayerCreationForm

    fieldsets = (
        (None,
            {'fields': ('email', 'username', 'password')}),
        ('Personal info',
            {'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'home_address',
                'home_zip',
                'work_address',
                'work_zip'
            )}),
        ('Permissions',
            {'fields': (
                'is_admin',
                'is_active',
                'last_login'
            )}),
    )

    list_display = [
        "username",
        "email",
        "last_login",
        "date_joined",
        "is_active",
    ]
    list_filter = ["date_joined", "username", ]
    search_fields = ["username", "email", ]
    ordering = ['date_joined']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
            )
        }),
    )


admin.site.unregister(Group)
