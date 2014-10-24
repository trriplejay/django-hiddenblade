from .models import Roster, Membership
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django import forms
from .forms import RosterCreationForm, RosterChangeForm
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
    #template_name = 'rosters/roster_detail.html'

    def get_queryset(self):
        return self.model.objects.live()

    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_authenticated() # &
#            request.user.id in self.get_queryset()
        ):
            return super(RosterDetailView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # HTTP 403

    def get_context_data(self, **kwargs):
        """
        Insert the needed objects into the context dict.

        """
        context = super(RosterDetailView, self).get_context_data(**kwargs)

        context['members'] = Membership.objects.filter(
            roster_id=context['object'].id
        )
        """context['mem_mod'] = Membership.objects.filter(
            roster_id=context['object'].id, is_moderator=True
        )"""
        return context
