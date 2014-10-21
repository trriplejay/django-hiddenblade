from .models import Roster, Membership
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django import forms


# Create your views here.
class RosterListView(ListView):
    model = Roster

    def get_queryset(self):
        return self.model.objects.live()


class RosterCreateView(CreateView):
    model = Roster


class RosterUpdateView(UpdateView):
    model = Roster

class RosterDetailView(DetailView):
    model = Roster
