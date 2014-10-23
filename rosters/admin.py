from django.contrib import admin

from .models import Roster, Membership
from .forms import RosterChangeForm, RosterCreationForm

# Register your models here.


class MembershipInline(admin.TabularInline):
    model = Membership
    fk_name = 'player'
    #extra = 1


@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):

    # getting weird error on the inline.. ignoring for now
#    inlines = (MembershipInline, )
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

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):

    #inlines = (MembershipInline, )
    #form = RosterChangeForm
    #add_form = RosterCreationForm

    fieldsets = (
        (None,
            {'fields': ('player','roster')}),
        ('Info',
            {'fields': (
                'invited_by',
            )}),
        ('Stats',
            {'fields': (
                'games_won',
                'frags',
                'deaths',
            )}),
        ('Fields with defaults',
            {'fields': (
                'is_moderator',
            )}),
    )

    list_display = [
        'player',
        'roster',
        'roster',
        'date_joined',
    ]

    list_filter = ["player", "roster", ]
    search_fields = ["name", "state", "city", ]
    ordering = ['date_joined']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'player',
                'roster',
                'invited_by',
                'is_moderator',
            )
        }),
    )