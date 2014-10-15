from .models import Player
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from .forms import PlayerForm
from django import forms

# Create your views here.


class LivePlayerMixin(object):
    def get_queryset(self):
        return self.model.objects.live()


class PlayerListView(LivePlayerMixin, ListView):
    model = Player


class PlayerDetailView(LivePlayerMixin, DetailView):
    model = Player
    slug_field = 'username'


class PlayerCreate(CreateView):
    model = Player
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    fields = (
        'username',
        'email',
        'phone_number',
        'first_name',
        'last_name',
        'home_address',
        'work_address',
    )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        player = super(PlayerCreate, self).save(commit=False)
        player.set_password(self.cleaned_data["password1"])
        if commit:
            player.save()
        return player

class PlayerUpdate(UpdateView):
    model = Player
    fields = ['email', 'home_address', 'work_address', 'phone_number']

class PlayerDelete(DeleteView):
    model = Player
    success_url = reverse_lazy('players')

"""
class PlayerFormView(FormView):
    form_class = PlayerForm
    template_name = "players/register.html"
    intial = {'key': 'value'}
    success_url = '/thanks/'

    def form_valid(self, form):
        return super(PlayerFormView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})
"""
