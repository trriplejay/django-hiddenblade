from django.conf.urls import patterns, url
from . import views
#from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', views.RosterListView.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.RosterDetailView.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/new-game$', views.GameCreateView.as_view(), name="newgame"),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/update$', views.RosterUpdateView.as_view(), name="rupdate"),
    url(r'^(?P<roster_id>\d+)/(?P<slug>[\w-]+)/game-cancel/(?P<pk>\d+)$', views.GameCancelView.as_view(), name="gcancel"),
    url(r'^(?P<roster_id>\d+)/(?P<slug>[\w-]+)/game-detail/(?P<pk>\d+)$', views.GameDetailView.as_view(), name="gdetail"),
    url(r'^(?P<roster_id>\d+)/(?P<slug>[\w-]+)/new-action/(?P<game_id>\d+)$', views.ActionCreateView.as_view(), name="akill"),
    url(r'^create/$', views.RosterCreateView.as_view(), name="create"),
)
