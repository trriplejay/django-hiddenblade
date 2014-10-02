from django.conf.urls import patterns, include, url
from . import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', views.PlayerListView.as_view(), name="list"),
    url(r'^(?P<slug>[\w-]+)/$', views.PlayerDetailView.as_view(), name="detail"),
   # url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)$', views.MyUserDetailView.as_view(), name="detail"),
   #url(r'^(?P<user_id>\d+)/$', views.MyUserDetailView.as_view(), name="detail"),

)
