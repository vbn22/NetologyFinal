# -*- coding: utf-8 -*-
from django import forms
from .models import Client,Subscriptions,Things
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('wallet',)


class SubscriptionsForm(forms.ModelForm):
    period_type = forms.ChoiceField(choices = Subscriptions.PERIOD_TYPE,required=False)
    class Meta:
        model = Subscriptions
        fields = ('things','period_type','days')

    def clean_days(self):
        period_type = self.cleaned_data.get("period_type")
        days = self.cleaned_data.get("days")
        if period_type and days:
            if len(days) > 2:
                raise forms.ValidationError("Вы выбрали больше двух дней")
            elif len(days) == 2 and int(period_type) != 2:
                raise forms.ValidationError("Вам нужно выбрать один день")
            elif len(days) == 1 and int(period_type) == 2:
                raise forms.ValidationError("Вам нужно выбрать два дня")
            elif len(days) == 0:
                raise forms.ValidationError("Вы не выбрали ниодного дня")
        return days

class SubscriptionsEditForm(SubscriptionsForm):
    class Meta:
        model = Subscriptions
        fields = ('things','period_type','days','status')
