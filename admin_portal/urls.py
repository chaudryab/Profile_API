 
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
     path('login_a', views.login_a, name='login_a'),
     path("index", views.index, name="index"),
]