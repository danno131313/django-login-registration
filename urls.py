from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^show$', views.show),
    url(r'^login$', views.login),
    url(r'^destroy/(?P<id>\d+)$', views.destroy),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^show/(?P<id>\d+)$', views.show_one),
    url(r'^update/(?P<id>\d+)$', views.update),
    url(r'^logout$', views.logout_user),
]
