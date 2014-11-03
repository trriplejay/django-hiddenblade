import sys
import random
from itertools import chain
from operator import attrgetter
from datetime import datetime
from django.db.models import Count, F
from django.http import HttpResponseRedirect
from .models import Roster, Membership, Game, Action, Comment
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django import forms
from .forms import RosterCreationForm, RosterChangeForm
from .forms import GameCreationForm, GameCancelForm
from .forms import ActionCreationForm
from .forms import CommentCreationForm
from .forms import MembershipCreationForm, MembershipRequestForm, MembershipApprovalForm, MembershipDenyForm
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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        If the user is not already a mod of 10 or more groups, allow
        them to create a new group
        """
        results = Membership.objects.get_mod_count(request.user.id)
        if results < 10:
            return super(RosterCreateView, self).dispatch(request, *args, **kwargs)
        else:
            # %TODO return special error saying that mod too many already
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
                'approved_by': self.request.user.username,
                'is_moderator': True
            })
        newmembership.save()
        return super(RosterCreateView, self).form_valid(theroster)

    def get_success_url(self):
        """
        redirect to the group list
        """

        # after a successful creation of the new group, redirect
        # the user to the group page, where their new group should
        # be listed at the very top
        return reverse_lazy('rosters:list')


class RosterUpdateView(UpdateView):
    template_name = 'rosters/roster_update.html'
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


class RosterDetailView(DetailView, FormView):
    model = Roster
    #template_name = 'rosters/roster_detail.html'

    def get_queryset(self):
        #print >>sys.stderr, self.kwargs

        # query for all members of this roster
        self.members = self.model.objects.get_all_members(
            self.kwargs['pk']
        ).order_by('-is_moderator', '-is_active', '-is_approved')

        # game logic, for when there is an active or recent game
        qs = Game.objects.get_recent_game(self.kwargs['pk'])
        # for this view, we only care about the most recent game
        results = list(qs[:1])
        self.target_username = None
        self.game_instance = None

        if results:
            self.game_instance = results[0]
            if self.game_instance.is_active:
                if self.game_instance.living_player_list == '':
                    self.living_players = []
                else:
                    self.living_players = self.game_instance.living_player_list.split(",")
                if self.game_instance.dead_player_list == '':
                    self.dead_players = []
                else:
                    self.dead_players = self.game_instance.dead_player_list.split(",")

                # find the current player's target by searching the
                # living player list looking for the logged in player.
                # The target will be the next index in the list
                try:
                    src_index = self.living_players.index(
                        str(self.request.user.username)
                    )
                except ValueError:
                    # player isn't active, so just give them a
                    # placeholder index.
                    src_index = 0
                if src_index == len(self.living_players) - 1:
                    tgt_index = 0
                else:
                    tgt_index = src_index + 1
                self.target_username = self.living_players[tgt_index]
        pendingcount = 0
        self.current_member = None
        self.is_member = False
        self.target_member = None
        for member in self.members:
            if member.player.username == self.request.user.username:
                self.current_member = member
                self.is_member = True
            if not member.is_approved:
                pendingcount += 1
            if self.target_username is not None:
                if member.player.username == self.target_username:
                    self.target_member = member
        self.pendingcount = pendingcount


        # get the action queryset
        actions = Action.objects.get_roster(self.kwargs['pk'])
        comments = Comment.objects.get_roster(self.kwargs['pk'])
        chained = chain(actions, comments)
        self.stream = sorted(chained, key=attrgetter('creation_time'), reverse=True)

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
        Insert the needed objects and values into the context.
        """

        context = super(RosterDetailView, self).get_context_data(**kwargs)
        current_username = self.request.user.username
        #print >>sys.stderr, thismember

        context['is_member'] = False

        if self.game_instance is not None:
            context['game'] = self.game_instance

            # if game is active, contextualize more info
            if self.game_instance.is_active:

                context['living_list'] = self.living_players
                context['living_len'] = len(self.living_players)

                context['dead_list'] = self.dead_players
                context['dead_len'] = len(self.dead_players)
                context['target'] = self.target_member

                #print >>sys.stderr, "target is: ", self.target_username

        context['members'] = self.members
        context['thismember'] = self.current_member
        context['is_member'] = self.is_member
        context['pending'] = self.pendingcount
        context['stream'] = self.stream

        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        #print >>sys.stderr, self.request.user.username
        if 'req_approval' in request.POST:
            newapproval = MembershipRequestForm(
                {
                    'player': self.request.user.id,
                    'roster': self.kwargs['pk'],
                    'is_approved': False,
                })
            newapproval.save()
        elif 'approve' in request.POST:
            # query to find this
            mem_id = request.POST['mem_id']
            #rost_id = self.kwargs['pk']
            Membership.objects.filter(
                id=mem_id).update(
                is_approved=True,
                approved_by=self.request.user.username
            )

        elif 'deny' in request.POST:
            # if denied, delete the membership?
            # best way to handle this would be to have a
            # separate model for denied memberships
            # %TODO
            pass

        elif 'deactivate' in request.POST:
            # user deactivating themselves
            # update membership to set is_active to False
            player_id = self.request.user.id
            rost_id = self.kwargs['pk']
            Membership.objects.filter(
                player=player_id,
                roster=rost_id
                ).update(
                is_active=False
            )
        elif 'activate_self' in request.POST:
            player_id = self.request.user.id
            rost_id = self.kwargs['pk']
            Membership.objects.filter(
                player=player_id,
                roster=rost_id
                ).update(
                is_active=True
            )

        elif 'new_status' in request.POST:
            # moderator is making a change to the
            # status of the group
            self.model.objects.filter(
                id=self.kwargs['pk']
                ).update(
                status=request.POST['new_status']
            )
        elif 'comment' in request.POST:
            # create a new comment
            newcomment = CommentCreationForm({
                'player': self.request.user.id,
                'text': request.POST['comment_text'],
                'roster': self.kwargs['pk']
            })
            newcomment.save()

        elif 'kill_tgt' in request.POST:
            """
            killing a target means the following:
              update game living/dead players list
              update source player kill count
              update target player death count
              check for end-of-game state (< 2 people left)
              create an action model instance of this event
            this means building 3-4 update queries
            and instantiating 1-2 create forms for actions
            hopefully nothing goes wrong in the middle....
            #%TODO best practices for this sort of thing?
            """
            # validate the form first
            self.get_queryset()
            # double check that the game is active, in case
            # we got here by black magic
            if self.game_instance.is_active:
                #remove target from living players list
                self.living_players.remove(str(self.target_username))
                #add target to the dead players list

                self.dead_players.append(str(self.target_username))

                living_list_formatted = ",".join(self.living_players)
                dead_list_formatted = ",".join(self.dead_players)
                #update the game to reflect the change
                completed = False
                if len(self.living_players) < 2:
                    # game is over, mark game as complete during update
                    completed = True
                if not completed:
                    Game.objects.filter(id=self.game_instance.id).update(
                        living_player_list=living_list_formatted,
                        dead_player_list=dead_list_formatted,
                    )
                else:
                    Game.objects.filter(id=self.game_instance.id).update(
                        living_player_list=living_list_formatted,
                        dead_player_list=dead_list_formatted,
                        completed=completed,
                        is_active=False,
                        end_time=datetime.now()
                    )

                src_mem_id = self.request.user.id
                tgt_mem_id = self.target_member.id
                # increment kills and possibly wins for source player
                # increment deaths and possibly losses for target player
                if not completed:
                    Membership.objects.filter(
                        id=src_mem_id
                        ).update(
                        frags=F('frags')+1,
                    )
                    Membership.objects.filter(
                        id=tgt_mem_id
                        ).update(
                        deaths=F('deaths')+1,
                    )
                else:
                    Membership.objects.filter(
                        id=src_mem_id
                        ).update(
                        frags=F('frags')+1,
                        games_won=F('games_won')+1
                    )

                    Membership.objects.filter(
                        id=tgt_mem_id
                        ).update(
                        deaths=F('deaths')+1,
                    )
                    # game is over, so increment every member's
                    # total games played
                    Membership.objects.filter(
                        is_active=True,
                        roster=self.kwargs['pk']
                        ).update(
                        total_games_played=F('total_games_played')+1
                    )

                # lastly, create an event (possibly two)
                # first even states A kills B, second event
                # may state that game has come to an end
                # instantiate endgame after kill so that the
                # timestamp will show the game ending after
                # the final assassination
                newaction = ActionCreationForm({
                    'source': self.request.user.id,
                    'target': self.target_member.player.id,
                    'flavor_text': request.POST['flavor_text'],
                    'game': self.game_instance.id,
                    'roster': self.kwargs['pk']
                })
                newaction.save()
                if completed:
                    the_text = "has emerged victorious!"

                    newaction = ActionCreationForm({
                        'source': self.request.user.id,
                        'target': self.request.user.id,
                        'flavor_text': the_text,
                        'game': self.game_instance.id,
                        'roster': self.kwargs['pk']
                    })
                    newaction.save()

        # refresh the same page we're already on
        #print >>sys.stderr, args, kwargs, request.POST
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
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


class GameDetailView(DetailView):
    model = Game


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

        context['members'] = Roster.objects.get_approved_members(
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
            if member.is_active:
                theList.append(member.player.username)
            #print >>sys.stderr, member.player

        theroster = context['roster']

        random.shuffle(theList)
        #print >>sys.stderr, theroster
        #print >>sys.stderr, ",".join(theList)

        self.results.living_player_list = ",".join(theList)
        self.results.roster = (list(theroster))[0]
        #print >>sys.stderr, form.instance.living_player_list

   #     player_id = self.request.user.id

        self.results.save()

        # create a new action to represent the start
        # of the game
        the_text = "has started the game!"
        newaction = ActionCreationForm({
            'source': self.request.user.id,
            'target': self.request.user.id,
            'flavor_text': the_text,
            'game': self.results.id,
            'roster': self.kwargs['pk']
        })
        newaction.save()

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
        if theGame.cancelled is True:
            theGame.completed = False
            theGame.is_active = False
            theGame.end_time = datetime.now()
            theGame.save()

            the_text = "has cancelled the game!"
            newaction = ActionCreationForm({
                'source': self.request.user.id,
                'target': self.request.user.id,
                'flavor_text': the_text,
                'game': self.kwargs['pk'],
                'roster': self.kwargs['roster_id']
            })
            newaction.save()
        return super(GameCancelView, self).form_valid(theGame)


class ActionCreateView(CreateView):
    template_name = 'rosters/action_form.html'
    model = Action
    form_class = ActionCreationForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #print >>sys.stderr, self.kwargs, self.args
        theroster = None
        if 'roster_id' in self.kwargs:
            theroster = self.kwargs['roster_id']
        #TODO add a check if theroster still = None after this section

        # check if the logged in user is in this group and is a moderator
        results = Membership.objects.get_mod_status(theroster, request.user.id).count()
        if results > 0:
            return super(GameCancelView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # HTTP 403

    def get_context_data(self, **kwargs):
        """
        Insert the needed objects into the context dict.

        """
        context = super(ActionCreateView, self).get_context_data(**kwargs)
        #print >>sys.stderr, self.kwargs, self.args
        thegame = None
        if 'game_id' in self.kwargs:
            thegame = self.kwargs['game_id']

        context['game'] = Game.objects.get(
            id=thegame,
            is_active=True
        )

        return context

    def form_valid(self, form):

        theAction = form.save(commit=False)
        theAction.source = False
        theAction.target = False

        theAction.save()
        return super(GameCancelView, self).form_valid(theAction)
