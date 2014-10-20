from .models import Roster, Membership
from django import forms


class RosterCreationForm(forms.ModelForm):
    """
    A form for creating new rosters. Includes all the required
    fields.
    """

    class Meta:
        model = Roster
        fields = (
            'name',
            'status',
            'description',
            'members',
            'city',
            'state',

        )

    def save(self, commit=True):
        # Save the provided password in hashed format
        roster = super(RosterCreationForm, self).save(commit=False)
        if commit:
            roster.save()
        return roster


class RosterChangeForm(forms.ModelForm):
    """A form for updating rosters.
    """

    class Meta:
        model = Roster
        fields = (
            'name',
            'status',
            'description',
            'members',
            'city',
            'state',
            'is_active',
        )
