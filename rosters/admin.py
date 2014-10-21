from django.contrib import admin

from .models import Roster, Membership
from .forms import RosterChangeForm, RosterCreationForm

# Register your models here.


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1

@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):

    inlines = (MembershipInline, )
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
                'zipcode'

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

