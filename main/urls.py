# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from django.contrib import admin
from main.views import Home,register,login,logout,\
    subscribe_buy,subscribe_list,subscribe_edit,subscribe_remove,subscribe_description,calculate,list_of_dates
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


urlpatterns = [
    url('^register/', register,name='register'),
    url('^login/', login,name='login'),
    url('^logout/', logout,name='logout'),

    url('^subscribe/buy', subscribe_buy,name='subscribe_buy'),
    url('^subscribe/edit/(\d+)', subscribe_edit,name='subscribe_edit'),
    url('^subscribe/remove/(\d+)', subscribe_remove,name='subscribe_remove'),
    url('^subscribe/description/(\d+)', subscribe_description,name='subscribe_description'),
    url('^subscribe/list', subscribe_list,name='subscribe_list'),
    url('^calculate/(\d+)/([-\w]+)', calculate,name='calculate'),
    url('^get_list_of_dates/(\d+)/([-\w]+)/([-\w]+)', list_of_dates,name='list_of_dates'),
    url(r'^', Home.as_view(),name='home'),
]