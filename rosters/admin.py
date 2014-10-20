from django.contrib import admin

from .models import Roster, Membership
from .forms import RosterChangeForm, RosterCreationForm

# Register your models here.


@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):

    form = RosterChangeForm
    add_form = RosterCreationForm

    fieldsets = (
        (None,
            {'fields': ('name',)}),
        ('Info',
            {'fields': (
                'description',
                'status',
                'city',
                'state',

            )}),
        ('Fields with defaults',
            {'fields': (
                'is_active',
            )}),
    )

    list_display = [
        'name',
        'city',
        'state',
        'status',
        'is_active',
    ]

    list_filter = ["name", "status", "city", "state", ]
    search_fields = ["name", "state", "city", ]
    ordering = ['date_created']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name',
                'members',
            )
        }),
    )
