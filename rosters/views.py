import sys
import random
from datetime import datetime
from django.db.models import Count
from .models import Roster, Membership, Game
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django import forms
from .forms import RosterCreationForm, RosterChangeForm
from .forms import GameCreationForm, GameCancelForm
from .forms import MembershipCreationForm
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import SingleObjectMixin

# Create your views here.
class RosterListView(ListView):
    model = Roster


class RosterCreateView(FormView):
    template_name = 'rosters/roster_form.html'
    form_class = RosterCreationForm
    model = Roster
    theroster = None

    def dispatch(self, request, *args, **kwargs):
        """
        If the user is not already a mod of 10 or more groups, allow
        them to create a new group
        """
        if (request.user.is_authenticated()):
            results = Membership.objects.get_mod_count(request.user.id)
            if results < 10:
                return super(RosterCreateView, self).dispatch(request, *args, **kwargs)
            else:
                # TODO return special error saying that mod too many already
                raise PermissionDenied  # HTTP 403
        else:
            raise PermissionDenied  # HTTP 403

    def form_valid(self, form):

        form.instance.user = self.request.user

        player_id = self.request.user.id

        theroster = form.save()
        roster_id = theroster.id
        newmembership = MembershipCreationForm(
            {
                'player': player_id,
                'roster': roster_id,
                'invited_by': self.request.user.username,
                'is_moderator': True
            })
        newmembership.save()
        return super(RosterCreateView, self).form_valid(self.roster)

    def get_success_url(self):
        """
        redirect to the group list
        """

        # after a successful creation of the new group, redirect
        # the user to the group page, where their new group should
        # be listed at the very top
        return reverse_lazy('rosters:list')


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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        # only check authentication here, since the group
        # might be public.  We also need to at least allow
        # the group name to be visible with an "request to
        # join" button.  We'll take care of that in the template.

        return super(RosterDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Insert the needed objects into the context.
        """
        context = super(RosterDetailView, self).get_context_data(**kwargs)
        thismember = self.request.user.id
        #print >>sys.stderr, thismember
        # query for all members of this roster
        members = self.model.objects.get_all_members(
            context['object'].id
        ).order_by('-is_moderator', '-is_active', '-is_approved')
        for member in members:
            if member.id == thismember:
                context['thismember'] = member
        context['members'] = members

        qs = Game.objects.get_recent_game(context['object'].id)
        result = list(qs[:1])
        if result:
            living_players = len(result[0].living_player_list.split(","))
            dead_players = result[0].dead_player_list.split(",")
            context['game'] = result[0]
            context['living_len'] = living_players
            context['dead_list'] = dead_players

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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #print >>sys.stderr, self.kwargs, self.args
        theroster = None
        if 'pk' in self.kwargs:
            theroster = self.kwargs['pk']
        #TODO add a check if theroster still = None after this section

        # check if the logged in user is in this group and is a moderator
        results = Roster.objects.get_mod_status(theroster, request.user.id).count()
        if results > 0:
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

        context['members'] = Roster.objects.get_active_members(
            theroster
        )
        if theroster is not None:
            context['roster'] = Roster.objects.get_roster(theroster)

        return context

    def form_valid(self, form):
        """
        build a list of all players in the group with active
        memberships, shuffle the list, then store it in the
        living_player_list
        """

        self.results = form.save(commit=False)

        theList = []
        #for member in self.request.context['members']:
        #    theList.append(member.username)

        #form.instance.living_player_list = theList
        #theList.shuffle()

        context = self.get_context_data()
        theList = []
        for member in context['members']:
            theList.append(member.player.username)
            #print >>sys.stderr, member.player

        theroster = context['roster']

        random.shuffle(theList)
        print >>sys.stderr, theroster
        print >>sys.stderr, ",".join(theList)

        self.results.living_player_list = ",".join(theList)
        self.results.roster = (list(theroster))[0]
        #print >>sys.stderr, form.instance.living_player_list

   #     player_id = self.request.user.id

        self.results.save()

        return super(GameCreateView, self).form_valid(form)


class GameCancelView(UpdateView):
    template_name = 'rosters/game_cancel.html'
    model = Game
    form_class = GameCancelForm

    def get_success_url(self):
        """
        redirect to the roster page after cancelling
        """

        if 'slug' in self.kwargs and 'roster_id' in self.kwargs:
            slug = self.kwargs['slug']
            pk = self.kwargs['roster_id']
            return reverse_lazy(
                'rosters:detail',
                kwargs={'pk': pk, 'slug': slug}
            )
        else:
            # if a player is updating without being able to access the slug
            # something else probably went wrong, so just send them home
            return reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #print >>sys.stderr, self.kwargs, self.args
        theroster = None
        if 'roster_id' in self.kwargs:
            theroster = self.kwargs['roster_id']
        #TODO add a check if theroster still = None after this section

        # check if the logged in user is in this group and is a moderator
        results = Roster.objects.get_mod_status(theroster, request.user.id).count()
        if results > 0:
            return super(GameCancelView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # HTTP 403

    def form_valid(self, form):

        theGame = form.save(commit=False)
        theGame.completed = False
        theGame.is_active = False
        theGame.end_time = datetime.now()
        theGame.save()
        return super(GameCancelView, self).form_valid(theGame)
