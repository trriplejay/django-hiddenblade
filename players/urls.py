from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change
from . import views
#from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^$', views.PlayerListView.as_view(), name="list"),
    url(r'^register/$', views.PlayerCreate.as_view(), name="register"),
    url(r'^(?P<slug>[\w-]+)/update/$', views.PlayerUpdate.as_view(), name="update"),
    url(r'^delete/$', views.PlayerDelete.as_view(), name="delete"),
    url(r'^(?P<slug>[\w-]+)/$', views.PlayerDetailView.as_view(), name="detail"),
    #url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)$', views.MyUserDetailView.as_view(), name="detail"),
    #url(r'^(?P<user_id>\d+)/$', views.MyUserDetailView.as_view(), name="detail"),
)
