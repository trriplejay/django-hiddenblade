from django.conf.urls import patterns, url
from . import views
#from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', views.RosterListView.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/(<slug>[\w-]+)/$', views.RosterDetailView.as_view(), name="detail"),
    url(r'^create/$', views.RosterCreateView.as_view(), name="create"),
)
