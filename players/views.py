from django.shortcuts import render
from .models import Player
from django.views.generic import ListView, DetailView, TemplateView

# Create your views here.


class LivePlayerMixin(object):
    def get_queryset(self):
        return self.model.objects.live()

class PlayerListView(LivePlayerMixin, ListView):
    model = Player 


class PlayerDetailView(DetailView):
    model = Player
    slug_field = 'username'
"""
class UserDetailView(TemplateView):
    template_name = "users/user_detail.html"
  #  model = User
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('user_id', None))
        return context
#    def get_queryset(self):
 #       return self.model.objects.get(pk)

"""
