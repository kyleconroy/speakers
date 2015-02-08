from django.conf.urls import include, url
from django.contrib import admin

from cfp import views


urlpatterns = [
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^conferences/new$',
        views.ConferenceCreate.as_view(),
        name='conference_create'
    ),
    url(
        r'^feed$',
        views.LatestCallsFeed(),
        name='call_feed'
    ),
    url(
        r'^(?P<year>\d+)/(?P<slug>[\w-]+)$',
        views.legacy,
        name='legacy_redirect'
    ),
    url(
        r'^(?P<slug>[\w-]+)/(?P<year>\d+)/call/new$',
        views.CallCreate.as_view(),
        name='call_create'
    ),
    url(
        r'^(?P<slug>[\w-]+)/(?P<year>\d+)/call/edit$',
        views.CallEdit.as_view(),
        name='call_edit'
    ),
    url(
        r'^(?P<slug>[\w-]+)/(?P<year>\d+)/edit$',
        views.ConferenceEdit.as_view(),
        name='conference_edit'
    ),
    url(
        r'^(?P<slug>[\w-]+)/(?P<year>\d+)$',
        views.CallDetail.as_view(),
        name='call_read'
    ),
    url(
        r'^$',
        views.CallList.as_view(),
        name='call_list'
    ),
]
