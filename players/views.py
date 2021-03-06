from .models import Player
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render
from django import forms
from rosters.models import Membership
from .forms import PlayerCreationForm, PlayerChangeForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login

# Create your views here.


class LivePlayerMixin(object):
    def get_queryset(self):
        return self.model.objects.live()


class PlayerListView(LivePlayerMixin, ListView):
    model = Player


class PlayerDetailView(LivePlayerMixin, DetailView):
    model = Player
    slug_field = 'username'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # need to test if currently logged in player is the
        # same as the profile we're attempting to load

        if kwargs['slug'] == request.user.username:
            return super(PlayerDetailView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # HTTP 403

    def get_context_data(self, **kwargs):
        """
        Insert the needed objects into the context.
        """
        context = super(PlayerDetailView, self).get_context_data(**kwargs)

        # query for all memberships for this player
        # and save the roster info for each.
        members = Membership.objects.get_member_groups(
            self.request.user.id
        )

        context['members'] = members
        """
        qs = Game.objects.get_recent_game(context['object'].id)
        result = list(qs[:1])
        living_players = len(result[0].living_player_list.split(","))
        dead_players = result[0].dead_player_list.split(",")
        context['game'] = result[0]
        context['living_len'] = living_players
        context['dead_list'] = dead_players
        """
        return context


class PlayerCreate(FormView):
    template_name = 'players/register.html'
    form_class = PlayerCreationForm
    model = Player

    def form_valid(self, form):
        """
        If we're in here, the form has been validated.  Save the form, and
        use the username/password to log the user in, now that they have
        been created
        """

        form.instance.user = self.request.user
        form.save()

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            if user.is_active:
                login(self.request, user)
            else:
                # users account is disabled, ask if they want to re-enable
                pass
        else:
            # authentication failed...
            pass

        return super(PlayerCreate, self).form_valid(form)

    def get_success_url(self):
        """
        Player was successfully created, and logged in, so redirect
        to their new profile
        """

        if self.request.user.is_authenticated:
            # Redirect the user's profile
            return reverse(
                'players:detail',
                kwargs={'slug': self.request.user.username}
            )
        else:
            # user didn't authenticate for some reason, send to login page
            return reverse('login')


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

