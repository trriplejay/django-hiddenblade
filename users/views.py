from django.shortcuts import render
from .models import User
from django.views.generic import ListView, DetailView

# Create your views here.


class LiveUserMixin(object):
    def get_queryset(self):
        return self.model.objects.live()

class UserListView(LiveUserMixin, ListView):
    model = User

class UserDetailView(LiveUserMixin, DetailView):
    model = User
