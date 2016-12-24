# -*- coding: utf-8 -*-
import unittest
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.test import Client as TestClient
from django.core.management import call_command
from .models import Things, Subscriptions


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
        return super(BusinessLogicTest,self).setUp(*args, **kwargs)

    def tearDown(self):
        Subscriptions.objects.all().delete()

    def test_buy_subscribe_with_one_thing(self):
        self.client.login(username=self.username, password=self.password)
        things_ids = Things.objects.filter(pk=1).values_list('id',flat=True)
        data = dict(things=things_ids)
        self.client.post('/subscribe/buy', data)
        sub_things_ids = self.user.profile.subscriptions.all()[0].things.values_list('id',flat=True)
        self.assertEqual(set(things_ids),set(sub_things_ids))

    def test_buy_subscribe_with_several_things(self):
        self.client.login(username=self.username, password=self.password)
        things_ids = Things.objects.all().values_list('id',flat=True)
        data = dict(things=things_ids)
        self.client.post('/subscribe/buy', data)
        sub_things_ids = self.user.profile.subscriptions.all()[0].things.values_list('id',flat=True)
        self.assertEqual(set(things_ids),set(sub_things_ids))