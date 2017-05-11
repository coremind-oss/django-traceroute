from django.conf.urls import url, include
from django.contrib import admin

from data import views


urlpatterns = [
    url(r'^(?P<domain>.*)$', views.traceroute, name='traceroute'),
    url(r'^experiment/$', views.experiment, name='experiment'),
]
