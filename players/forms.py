from .models import Player
from django import forms


class PlayerForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = Player
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'phone_number',
            'first_name',
            'last_name',
            'home_address',
            'work_address',
        )


