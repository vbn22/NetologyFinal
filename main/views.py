# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse,Http404
from django.shortcuts import render_to_response
from django.contrib import  auth
from django.contrib.auth.models import user_logged_in
from main.models import *
from main import *
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self):
        return dict(title='Hello World')

