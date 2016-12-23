# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from django.contrib import admin
from main.views import Home
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


urlpatterns = [
    url('^register/', 'main.views.register',name='register'),
    url('^login/', 'main.views.login',name='login'),
    url(r'^', Home.as_view(),name='home'),
]