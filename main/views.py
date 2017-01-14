# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import UserForm,ClientForm,SubscriptionsForm,SubscriptionsEditForm
from .models import Subscriptions
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta
import json


@login_required
def calculate(request,id,date):
    result_calculate = 0
    subscription = Subscriptions.objects.get(pk=id)
    subscription_days = subscription.days.values_list('day',flat=True)
    price_per_day = sum(subscription.things.values_list('price',flat=True))
    time_length = datetime.strptime(date,'%Y-%m-%d') - subscription.date_of_purchase.replace(tzinfo=None)
    for iter_day in range(1,time_length.days+1):
        iter_date = subscription.date_of_purchase + timedelta(days=iter_day)
        if iter_date.day in subscription_days:
            result_calculate += price_per_day

    return render(request, 'subscribe_description.html', {
        'date_calculate':date,
        'result_calculate':result_calculate,
        'subscription': subscription,
        'period_type':[x[1] for x in Subscriptions.PERIOD_TYPE if x[0] == subscription.period_type]
    })

@login_required
def list_of_dates(request,id,number_of_months,start_date):
    subscription = Subscriptions.objects.get(pk=id)
    list_of_dates = []
    days = [datetime.strptime(start_date,'%Y-%d-%m').replace(day=item.day) for item in subscription.days.all()]
    for month in range(0,int(number_of_months)):
         list_of_dates.extend([(day+relativedelta(months=month)).strftime('%m/%d/%Y') for day in days])
    data = json.dumps(dict(list_of_dates=list_of_dates))
    return HttpResponse(data,content_type='application/json')

@login_required
def subscribe_description(request,id):
    subscription = Subscriptions.objects.get(pk=id)
    return render(request, 'subscribe_description.html', {
        'subscription': subscription,
        'period_type':[x[1] for x in Subscriptions.PERIOD_TYPE if x[0] == subscription.period_type]
    })



@login_required
def subscribe_remove(request,id):
    Subscriptions.objects.filter(pk=id).delete()
    messages.success(request, ('Подписка удалена !'))
    return redirect('/subscribe/list')

@login_required
def subscribe_edit(request,id):
    if request.POST:
        subscribe_form = SubscriptionsEditForm(request.POST,instance=Subscriptions.objects.get(pk=id))
    else:
        subscribe_form = SubscriptionsEditForm(instance=Subscriptions.objects.get(pk=id))
    if request.POST and subscribe_form.is_valid():
        subscribe = subscribe_form.save()
        messages.success(request, ('Изменения сохранены !'))
        return redirect('/subscribe/list')
    return render(request, 'subscribe.html', {
        'subscribe_form': subscribe_form,
    })

@login_required
def subscribe_list(request):
    subscriptions = request.user.profile.subscriptions.all()
    return render(request,'subscriptions.html',dict(subscriptions=subscriptions))


@login_required
def subscribe_buy(request):
    subscribe_form = SubscriptionsForm(request.POST)
    if request.POST and subscribe_form.is_valid():
        subscribe = subscribe_form.save()
        subscribe.user = request.user.profile
        subscribe.save()
        messages.success(request, ('Ваш заказ принят !'))
        return redirect('/')
    return render(request, 'subscribe.html', {
        'subscribe_form': subscribe_form,
    })

@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')


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
    template_name = "index.html"

    def get_context_data(self):
        title = 'Сервис продажи бритвенных станков'
        user = self.request.user
        return dict(title=title,user=user)

