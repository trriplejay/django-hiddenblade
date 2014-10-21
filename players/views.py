from .models import Player
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django import forms
from .forms import PlayerCreationForm, PlayerChangeForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.


class LivePlayerMixin(object):
    def get_queryset(self):
        return self.model.objects.live()


class PlayerListView(LivePlayerMixin, ListView):
    model = Player


class PlayerDetailView(LivePlayerMixin, DetailView):
    model = Player
    slug_field = 'username'

    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_authenticated() &
            request.path_info.find(
                request.user.username
            ) != -1
        ):
            return super(PlayerDetailView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # HTTP 403


class PlayerCreate(FormView):
    template_name = 'players/register.html'
    form_class = PlayerCreationForm
    success_url = '/thanks'
    model = Player

   # def get_form(self, form_class):
    """
    Check if the user already saved contact details. If so, then show
    the form populated with those details, to let user change them.
    """
#        try:
            #player = Player.objects.get(player=self.request.player)
 #           return form_class(instance=player, **self.get_form_kwargs())
  #      except Player.DoesNotExist:
    #        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(PlayerCreate, self).form_valid(form)

"""
    fields = (
        'username',
        'email',
        'password',
        'phone_number',
        'first_name',
        'last_name',
        'home_address',
        'work_address',
        'date_joined',
    )
"""


class PlayerUpdate(UpdateView):
    model = Player
    template_name = 'players/update.html'
    form_class = PlayerChangeForm
    success_url = 'players:detail'
    slug_field = 'username'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlayerUpdate, self).dispatch(*args, **kwargs)




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
