# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from django.contrib import admin
from main.views import Home,register,login,logout,subscribe_buy,subscribe_list,subscribe_edit,subscribe_remove
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


urlpatterns = [
    url('^register/', register,name='register'),
    url('^login/', login,name='login'),
    url('^logout/', logout,name='logout'),

    url('^subscribe/buy', subscribe_buy,name='subscribe_buy'),
    url('^subscribe/edit/(\d+)', subscribe_edit,name='subscribe_edit'),
    url('^subscribe/remove/(\d+)', subscribe_remove,name='subscribe_remove'),
    url('^subscribe/list', subscribe_list,name='subscribe_list'),
    url(r'^', Home.as_view(),name='home'),
]