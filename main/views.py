# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import UserForm,ClientForm
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, ('Вы успешно авторизовались'))
            return redirect('/')
        else:
            messages.success(request, ('Такой пользователь не найден'))
    return render(request, 'login.html')



def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        client_form = ClientForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data["password1"])
            user.save()
            profile = client_form.save()
            profile.user = user
            profile.save()
            messages.success(request, ('Вы успешно зарегестрированы!'))
            return redirect('/')
        else:
            messages.error(request, ('Пожалуйста, проверьте правильность данных!'))
    else:
        user_form = UserForm()
        client_form = ClientForm()
    return render(request, 'register.html', {
        'user_form': user_form,
        'client_form': client_form
    })


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self):
        return dict(title='Сервис продажи бритвенных станков')

