from django.conf.urls import url
from . import views
from .views import create_mailing, track_email_open

urlpatterns = [
    url(r'^$', views.create_mailing, name='create_mailing'),
    url(r'^track/(?P<mailing_id>\d+)/(?P<tracking_token>[0-9a-f-]+)/$', views.track_email_open, name='track_email_open'),
    url(r'^create/$', views.create_mailing, name='create_mailing'),
    url(r'^list/$', views.mailing_list, name='mailing_list'),
    url(r'^(?P<mailing_id>\d+)/$', views.mailing_detail, name='mailing_detail'),
]
