from django.contrib import admin

from .models import Roster, Membership, Game
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
            {'fields': ('player', 'roster')}),
        ('Info',
            {'fields': (
                'approved_by',
                'is_active',
                'is_approved'
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
                'approved_by',
                'is_moderator',
            )
        }),
    )

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):

    #inlines = (MembershipInline, )
    #form = RosterChangeForm
    #add_form = RosterCreationForm

    fieldsets = (
        (None,
            {'fields': ('end_time',)}),
        ('Info',
            {'fields': (
                'living_player_list',
                'dead_player_list',
                'house_rules',
                'completed',
                'cancelled',
                'mode',
                'roster'
            )}),
    )

    list_display = [
        'start_time',
        'mode',
    ]

    list_filter = ["start_time", "mode", ]
    search_fields = ["mode", ]
    ordering = ['start_time']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'roster',
                'living_player_list',
                'invited_by',
                'house_rules',
            )
        }),
    )