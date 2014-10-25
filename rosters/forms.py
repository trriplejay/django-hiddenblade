from .models import Roster, Membership, Game
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
            'members',
            'city',
            'state',
            'zipcode',
            'is_active',
        )


class MembershipCreationForm(forms.ModelForm):

    class Meta:
        model = Membership
        fields = (
            'player',
            'roster',
            'invited_by',
            'is_moderator'
        )
"""
    def save(self, commit=True):

        membership = super(MembershipCreationForm, self).save(commit=False)

        if commit:
            membership.save()
        return membership
"""


class GameCreationForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = (
            'mode',
            'house_rules'
            )
