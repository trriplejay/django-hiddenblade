from .models import Roster, Membership
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django import forms
from .forms import RosterCreationForm, RosterChangeForm
from .forms import MembershipCreationForm
from django.core.urlresolvers import reverse_lazy

# Create your views here.
class RosterListView(ListView):
    model = Roster


class RosterCreateView(FormView):
    template_name = 'rosters/roster_form.html'
    form_class = RosterCreationForm
    model = Roster
    succes_url = '/thanks/'

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
                'invited_by': self.request.user.id,
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

    def get_queryset(self):
        return self.model.objects.get_players_members()
