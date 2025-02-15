from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('create/', views.create_mailing, name='create_mailing'),
    url('list/', views.mailing_list, name='mailing_list'),
    url(r'^(?P<mailing_id>\d+)/$', views.mailing_detail, name='mailing_detail'),
]
