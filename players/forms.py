from .models import Player
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from localflavor.us.forms import USPhoneNumberField
from localflavor.us.forms import USZipCodeField
from localflavor.us.forms import USStateSelect


class PlayerCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )
    phone_number = USPhoneNumberField(required=False)
    state = USStateSelect()
    home_zip = USZipCodeField(required=False)
    work_zip = USZipCodeField(required=False)

    class Meta:
        model = Player
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'phone_number',
            'home_address',
            'state',
            'home_zip',
            'work_address',
            'work_zip',

        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(PlayerCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PlayerChangeForm(forms.ModelForm):
    """
    A form for updating users. Passwords are updated separately
    """

    phone_number = USPhoneNumberField(required=False)
    state = USStateSelect()
    home_zip = USZipCodeField(required=False)
    work_zip = USZipCodeField(required=False)

    class Meta:
        model = Player
        fields = (
            'username',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'home_address',
            'home_zip',
            'work_address',
            'work_zip',
        )

    def clean_password(self):
        # return original password
        return self.initial['password']

    def save(self, commit=True):
        user = super(PlayerChangeForm, self).save(commit=False)

        if commit:
            user.save()
        return user
