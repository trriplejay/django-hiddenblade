from .models import Roster, Membership, Game, Action, Comment
from django import forms
from localflavor.us.forms import USZipCodeField
from localflavor.us.forms import USStateSelect
from django.views.generic import FormView




class RosterCreationForm(forms.ModelForm):
    """
    A form for creating new rosters. Includes all the required
    fields.
    """

    state = USStateSelect()
    zipcode = USZipCodeField(required=False)

    class Meta:
        model = Roster
        fields = (
            'name',
            'status',
            'description',
            'city',
            'state',
            'zipcode',

        )

    def save(self, commit=True):

        roster = super(RosterCreationForm, self).save(commit=False)
        #need to set the current user as the creator/moderator of the group
        #this is done in the view, the roster must be created already
        #so that a moderator membership can be created specifying this
        #roster's ID

        if commit:
            roster.save()
        return roster


class RosterChangeForm(forms.ModelForm):
    """A form for updating rosters.
    """

    state = USStateSelect()
    zipcode = USZipCodeField(required=False)

    class Meta:
        model = Roster
        fields = (
            'name',
            'status',
            'description',
            'city',
            'state',
            'zipcode',
        )


class MembershipCreationForm(forms.ModelForm):

    class Meta:
        model = Membership
        fields = (
            'player',
            'roster',
            'approved_by',
            'is_moderator',
        )


class MembershipRequestForm(forms.ModelForm):

    class Meta:
        model = Membership
        fields = (
            'player',
            'roster',
            'is_approved',
        )


class MembershipApprovalForm(forms.ModelForm):

    class Meta:
        model = Membership
        fields = (
            'player',
            'roster',
            'is_approved',
        )


class MembershipDenyForm(forms.ModelForm):

    class Meta:
        model = Membership
        fields = (
            'player',
            'roster',
            'is_approved',
        )


class GameCreationForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = (
            'mode',
            'house_rules',
            'living_player_list'
            )

    def save(self, commit=True):

        self.instance.living_player_list

        game = super(GameCreationForm, self).save(commit=False)
        # need to set the living player list to be all the active
        # members of the group

        if commit:
            game.save()
        return game

class GameCancelForm(forms.ModelForm):
    """A form for cancelling an active game.
    """

    class Meta:
        model = Game
        fields = (
            'cancelled',
        )


class ActionKillForm(forms.ModelForm):
    """A form for a player to kill their target
    """
    class Meta:
        model = Action
        fields = (
            'flavor_text',
        )
