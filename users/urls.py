from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.UserListView.as_view(), name="list"),
   #url(r'^(?P<username>[\w-]+)/$', views.UserDetailView.as_view(), name="detail"),
    url(r'^(?P<id>\d)/$', views.UserDetailView.as_view(), name="detail"),

)
