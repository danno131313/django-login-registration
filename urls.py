from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='user_index'),
    url(r'^register$', views.register, name='user_register'),
    url(r'^show$', views.show, name='user_show'),
    url(r'^login$', views.login, name='user_login'),
    url(r'^destroy/(?P<id>\d+)$', views.destroy, name='user_destroy'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='user_edit'),
    url(r'^show/(?P<id>\d+)$', views.show_one, name='user_show_one'),
    url(r'^update/(?P<id>\d+)$', views.update, name='user_update'),
    url(r'^logout$', views.logout_user, name='user_logout'),
]
