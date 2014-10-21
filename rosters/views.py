from .models import Roster, Membership
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django import forms
from .forms import RosterCreationForm



# Create your views here.
class RosterListView(ListView):
    model = Roster

    def get_queryset(self):
        return self.model.objects.live()


class RosterCreateView(FormView):
    template_name = 'rosters/roster_form.html'
    form_class = RosterCreationForm
    model = Roster
    succes_url = '/thanks/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(RosterCreate, self).form_valid(form)

class RosterUpdateView(UpdateView):
    model = Roster

class RosterDetailView(DetailView):
    model = Roster
