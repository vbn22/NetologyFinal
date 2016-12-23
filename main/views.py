# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse,Http404
from django.shortcuts import render_to_response
from django.contrib import  auth
from django.contrib.auth.models import user_logged_in
from main.models import *
from main import *


def home(request,page = 1):
    args = {}
    return render_to_response('home.html',dict(title='Hello World'))

