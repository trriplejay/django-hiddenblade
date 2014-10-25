import sys
from django.db.models import Count
from .models import Roster, Membership, Game
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django import forms
from .forms import RosterCreationForm, RosterChangeForm
from .forms import GameCreationForm
from .forms import MembershipCreationForm
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin

# Create your views here.
class RosterListView(ListView):
    model = Roster


class RosterCreateView(FormView):
    template_name = 'rosters/roster_form.html'
    form_class = RosterCreationForm
    model = Roster

    def form_valid(self, form):
        """
        make sure to check if this user is moderator of more than 10 groups
        """
        form.instance.user = self.request.user

        player_id = self.request.user.id

        roster = form.save()
        roster_id = roster.id
        newmembership = MembershipCreationForm(
            {
                'player': player_id,
                'roster': roster_id,
                'invited_by': self.request.user.username,
                'is_moderator': True
            })
        newmembership.save()
        return super(RosterCreateView, self).form_valid(form)

    def get_success_url(self):
        """
        redirect to the roster page after creating
        """

        if 'slug' in self.kwargs and 'pk' in self.kwargs:
            slug = self.kwargs['slug']
            pk = self.kwargs['pk']
            return reverse_lazy(
                'rosters:detail',
                kwargs={'pk': pk, 'slug': slug}
            )
        else:
            # if a player is updating without being able to access the slug
            # something else probably went wrong, so just send them home
            return reverse_lazy('home')


class RosterUpdateView(FormView):
    template_name = 'rosters/update.html'
    model = Roster
    form_class = RosterChangeForm

    def get_success_url(self):
        """
        redirect to the roster page after updating
        """

        if 'slug' in self.kwargs and 'pk' in self.kwargs:
            slug = self.kwargs['slug']
            pk = self.kwargs['pk']
            return reverse_lazy(
                'rosters:detail',
                kwargs={'pk': pk, 'slug': slug}
            )
        else:
            # if a player is updating without being able to access the slug
            # something else probably went wrong, so just send them home
            return reverse_lazy('home')


class RosterDetailView(DetailView):
    model = Roster
    #template_name = 'rosters/roster_detail.html'

    def get_queryset(self):
        return self.model.objects.live()

    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_authenticated()):
            # only check authentication here, since the group
            # might be public.  We also need to at least allow
            # the group name to be visible with an "request to
            # join" button.  We'll take care of that in the template.

            return super(RosterDetailView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # HTTP 403

    def get_context_data(self, **kwargs):
        """
        Insert the needed objects into the context.
        """
        context = super(RosterDetailView, self).get_context_data(**kwargs)

        # query for all members of this roster
        context['members'] = self.model.objects.get_all_members(
            context['object'].id
        )
        return context


class GameCreateView(FormView):
    form_class = GameCreationForm
    template_name = 'rosters/game_form.html'
    model = Game

    def get_success_url(self):
        """
        redirect to the roster page after creating the game
        """

        if 'slug' in self.kwargs and 'pk' in self.kwargs:
            slug = self.kwargs['slug']
            pk = self.kwargs['pk']
            return reverse_lazy(
                'rosters:detail',
                kwargs={'pk': pk, 'slug': slug}
            )
        else:
            # if a player is starting a new game without being able to
            # access the slug something else probably went wrong, so
            # just send them home
            return reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        #print >>sys.stderr, self.kwargs, self.args
        theroster = None
        if 'pk' in self.kwargs:
            theroster = self.kwargs['pk']
        # check if the logged in user is in this group and is a moderator
        results = Roster.objects.get_mod_status(theroster, request.user.id).count()
        print >>sys.stderr, results
        if (request.user.is_authenticated() and
            results > 0
        ):
            return super(GameCreateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # HTTP 403

    def get_context_data(self, **kwargs):
        """
        Insert the needed objects into the context dict.

        """
        context = super(GameCreateView, self).get_context_data(**kwargs)
        #print >>sys.stderr, self.kwargs, self.args
        theroster = None
        if 'pk' in self.kwargs:
            theroster = self.kwargs['pk']
        #context['members'] = Membership.objects.filter(
#            roster_id=theroster, is_active=True
 #       )
        context['members'] = Roster.objects.get_active_members(
            theroster
        )

        return context

    def form_valid(self, form):
        """
        build a list of all players in the group with active
        memberships, shuffle the list, then store it in the
        living_players_list
        """
        form.instance.user = self.request.user

        player_id = self.request.user.id

        game = form.save()

        return super(RosterCreateView, self).form_valid(form)
