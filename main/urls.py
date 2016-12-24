# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from django.contrib import admin
from main.views import Home,register,login,logout,subscribe_buy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


urlpatterns = [
    url('^register/', register,name='register'),
    url('^login/', login,name='login'),
    url('^logout/', logout,name='logout'),

    url('^subscribe/buy', subscribe_buy,name='subscribe_buy'),
    url(r'^', Home.as_view(),name='home'),
]