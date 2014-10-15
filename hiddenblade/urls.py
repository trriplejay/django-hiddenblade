from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hiddenblade.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.HomepageView.as_view(), name="home"),
    url(r'^players/', include("players.urls", namespace="players")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^thanks/', views.ThanksView.as_view(), name="thanks"),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout")
)
