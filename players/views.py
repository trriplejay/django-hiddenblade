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
    model = Player

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(PlayerCreate, self).form_valid(form)

    def get_success_url(self):
        """
        redirect to the player's profile after updating
        """

        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            return reverse_lazy('players:detail', kwargs={'slug': slug})
        else:
            # if a player is updating without being able to access the slug
            # something else probably went wrong, so just send them home
            return reverse_lazy('home')


class PlayerUpdate(UpdateView):
    model = Player
    template_name = 'players/update.html'
    slug_field = 'username'
    form_class = PlayerChangeForm
    #success_url = reverse_lazy('detail')


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.username == kwargs['slug']:
            return super(PlayerUpdate, self).dispatch(*args, **kwargs)
        else:
            raise PermissionDenied  # HTTP 403

    def get_success_url(self):
        """
        redirect to the player's profile after updating
        """

        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            return reverse_lazy('players:detail', kwargs={'slug': slug})
        else:
            # if a player is updating without being able to access the slug
            # something else probably went wrong, so just send them home
            return reverse_lazy('home')


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
