# -*- coding: utf-8 -*-
import unittest
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.test import Client as TestClient
from django.core.management import call_command
from .models import Things, Subscriptions, Days


class UserAuthTest(unittest.TestCase):
    email = 'email@email.ru'
    password = '123123'
    username = 'testuser'
    user = None

    def setUp(self):
        self.client = TestClient()

    def prepare_db(self):
        call_command('loaddata', 'user.json', verbosity=0)
        call_command('loaddata', 'client.json', verbosity=0)
        self.user = User.objects.get(username=self.username)
        return self.user

    def test_client_can_register(self):
        data = dict(username=self.username,
                    wallet=100,
                    last_name='last_name',
                    email=self.email,
                    password1=self.password,
                    password2=self.password
                    )
        self.client.post('/register/',data)
        self.assertTrue(User.objects.filter(email=self.email))

    def test_login_client(self):
        self.prepare_db()
        data = dict(username=self.username,password=self.password)
        self.client.post('/login/',data)
        self.assertTrue(get_user(self.client).is_authenticated())

    def test_logout(self):
        self.prepare_db()
        self.client.login(username=self.username, password=self.password)
        self.client.get('/logout/')
        self.assertTrue(get_user(self.client).is_anonymous())


class BusinessLogicTest(UserAuthTest):
    def setUp(self,*args, **kwargs):
        self.prepare_db()
        call_command('loaddata', 'things.json', verbosity=0)
        call_command('loaddata', 'days.json', verbosity=0)
        super(BusinessLogicTest,self).setUp(*args, **kwargs)
        self.client.login(username=self.username, password=self.password)

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

    def test_page_with_list_of_subscriptions(self):
        response = self.client.get('/subscribe/list')
        self.assertTrue(response.context['subscriptions'])