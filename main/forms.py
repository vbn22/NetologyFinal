# -*- coding: utf-8 -*-
from django import forms
from .models import Client
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'email')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('wallet',)