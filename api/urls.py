from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('signup', views.users, name='signup'),
    path('signin', views.login, name='signin'),
    path('meetings', views.meetings, name='meetings'),
    path('links', views.social_links, name='links'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('admin_login', views.admin_login, name='admin_login'),
    path("logout", views.logout, name="logout"),
    path("index", views.index, name="index"),
    path("customers", views.customers, name="customers"),
    path('c_meetings', views.c_meetings, name='c_meetings'),
    path('user_detail/<pk>', views.user_detail, name='user_detail'),
    path('user_delete/<pk>', views.user_delete, name='user_delete'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('forget_change_pwd/<str:token>', views.forget_change_pwd, name='forget_change_pwd'),
    path('admin_change_pwd',views.admin_change_pwd,name='admin_change_pwd'),
    path('admin_forget_pwd',views.admin_forget_pwd,name='admin_forget_pwd'),
    path('admin_reset_pwd',views.admin_reset_pwd,name='admin_reset_pwd'),
    path('success',views.success,name='success'),
    path('myprofile',views.myprofile,name='myprofile')
]
