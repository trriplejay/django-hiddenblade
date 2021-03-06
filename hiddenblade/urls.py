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
    url(r'^groups/', include("rosters.urls", namespace="rosters")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^thanks/$', views.ThanksView.as_view(), name="thanks"),
    url(r'^about/$', views.AboutView.as_view(), name="about"),
    url(
        r'^login/$', 'django.contrib.auth.views.login', {
            'template_name': 'login.html'
        }, name="login"
    ),
    url(
        r'^logout/$', 'django.contrib.auth.views.logout', {
            'template_name': 'logout.html'
        }, name="logout"
    ),
    url(
        r'^password_change/$',
        'django.contrib.auth.views.password_change', {
            'template_name': 'password_change.html'
        }, name="password_change"
    ),
    url(
        r'^password_change_done/$',
        'django.contrib.auth.views.password_change_done',{
            'template_name': 'password_change_done.html'
        },
        name="password_change_done"
    ),
)

urlpatterns += patterns('',
    (r'^static/(.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),

)
