from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.users, name='signup'),
    path('signin', views.login, name='signin'),
    path('meetings', views.meetings, name='meetings'),
    path('links', views.social_links, name='links'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('change_password', views.change_password, name='change_password'),

]