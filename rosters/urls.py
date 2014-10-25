from django.conf.urls import patterns, url
from . import views
#from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', views.RosterListView.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.RosterDetailView.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/new-game$', views.GameCreateView.as_view(), name="newgame"),
    url(r'^create/$', views.RosterCreateView.as_view(), name="create"),
)
