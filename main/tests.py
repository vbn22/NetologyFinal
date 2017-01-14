# -*- coding: utf-8 -*-
import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.test import Client as TestClient
from django.core.management import call_command
from .models import Things, Subscriptions, Days
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

email = 'email@email.ru'
password = '123123'
username = 'testuser'
last_name = 'last_name'

class UserAuthTest(TestCase):
    fixtures = ['user.json','client.json']
    client,user = None,None

    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.get(username=username)

    def test_client_can_register(self):
        username2 = 'username2'
        email2 = 'test2@test.ru'
        data = dict(username=username2,
                    wallet=100,
                    last_name=last_name,
                    email=email2,
                    password1=password,
                    password2=password
                    )
        self.client.post('/register/',data)
        self.assertTrue(User.objects.filter(username=username2))

    def test_login_client(self):
        data = dict(username=username,password=password)
        self.client.post('/login/',data)
        self.assertTrue(get_user(self.client).is_authenticated())

    def test_logout(self):
        self.client.login(username=username, password=password)
        self.client.get('/logout/')
        self.assertTrue(get_user(self.client).is_anonymous())


class CreateSubscriptionTest(TestCase):
    fixtures = ['user.json','client.json','things.json','days.json']
    client,user = None,None

    def setUp(self,*args, **kwargs):
        self.client = TestClient()
        self.client.login(username=username, password=password)
        self.user = User.objects.get(username=username)

    def tearDown(self):
        Subscriptions.objects.all().delete()

    def test_buy_subscribe_with_one_thing(self):
        things_ids = Things.objects.filter(pk=1).values_list('id',flat=True)
        self.client.post('/subscribe/buy', dict(things=things_ids))
        sub_things_ids = self.user.profile.subscriptions.all()[0].things.values_list('id',flat=True)
        self.assertEqual(set(things_ids),set(sub_things_ids))

    def test_buy_subscribe_with_several_things(self):
        things_ids = Things.objects.all().values_list('id',flat=True)
        self.client.post('/subscribe/buy', dict(things=things_ids))
        sub_things_ids = self.user.profile.subscriptions.all()[0].things.values_list('id',flat=True)
        self.assertEqual(set(things_ids),set(sub_things_ids))

    def test_subscribe_with_type_period(self):
        period_type = Subscriptions.PERIOD_TYPE[0][0]
        self.client.post('/subscribe/buy', dict(period_type=period_type))
        sub_period_type = self.user.profile.subscriptions.all()[0].period_type
        self.assertEqual(period_type,sub_period_type)

    def test_subscribe_with_days(self):
        days_ids = Days.objects.filter(day__in=[1,3]).values_list('id',flat=True)
        self.client.post('/subscribe/buy', dict(days=days_ids))
        sub_days_ids = self.user.profile.subscriptions.all()[0].days.values_list('id',flat=True)
        self.assertEqual(set(days_ids),set(sub_days_ids))


class EditSubscriptionTest(TestCase):
    fixtures = ['user.json','client.json','things.json','days.json','subscriptions.json']
    client,user,subscription_id = None,None,None

    def setUp(self,*args, **kwargs):
        self.client = TestClient()
        self.client.login(username=username, password=password)
        self.user = User.objects.get(username=username)
        self.subscription_id = self.user.profile.subscriptions.all()[0].id

    def tearDown(self):
        Subscriptions.objects.all().delete()

    def test_page_with_list_of_subscriptions(self):
        response = self.client.get('/subscribe/list')
        self.assertTrue(response.context['subscriptions'])

    def test_page_edit_subscription(self):
        response = self.client.get('/subscribe/edit/'+str(self.subscription_id))
        self.assertTrue(response.context['subscribe_form'])

    def test_change_days_in_subscription(self):
        new_days_ids = Days.objects.filter(day__in=[2,25]).values_list('id',flat=True)
        self.client.post('/subscribe/edit/'+str(self.subscription_id),dict(days=new_days_ids))
        sub_new_days_ids = self.user.profile.subscriptions.all()[0].days.values_list('id',flat=True)
        self.assertEqual(set(new_days_ids),set(sub_new_days_ids))

    def test_change_status_subscription(self):
        status = False
        self.client.post('/subscribe/edit/'+str(self.subscription_id),dict(status=status))
        sub_status = self.user.profile.subscriptions.all()[0].status
        self.assertEqual(status,sub_status)

    def test_remove_subscription(self):
        self.client.get('/subscribe/remove/'+str(self.subscription_id))
        self.assertFalse(self.user.profile.subscriptions.all())


class PriceTest(TestCase):
    fixtures = ['user.json','client.json','things.json','days.json','subscriptions.json']
    client,user,subscription,subscription_id = None,None,None,None

    def setUp(self,*args, **kwargs):
        self.client = TestClient()
        self.client.login(username=username, password=password)
        self.user = User.objects.get(username=username)
        self.subscription = self.user.profile.subscriptions.all()[0]
        self.subscription_id = self.subscription.id

    def test_calculate_price_for_date(self):
        date = datetime.strptime('2017-02-01','%Y-%m-%d')
        date_of_purchase = self.subscription.date_of_purchase #2016-12-24
        url = '/calculate/'+str(self.subscription_id)+'/'+date.strftime('%Y-%m-%d')
        response = self.client.get(url)
        self.assertEqual((1+8)+(1+8),int(response.context['result_calculate']))


    def test_get_list_of_dates(self):
        number_of_months = 1
        start_date = '2017-01-01'
        url = '/get_list_of_dates/%s/%s/%s'%(self.subscription_id,number_of_months,start_date)
        response = self.client.get(url)
        list_of_dates = ['1/3/2017','1/10/2017']
        self.assertEqual(set(list_of_dates),set(response.context['list_of_dates']))
