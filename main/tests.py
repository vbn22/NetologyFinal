# -*- coding: utf-8 -*-
import unittest
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.test import Client as TestClient
from django.core.management import call_command

class UserAuthTest(unittest.TestCase):
    email = 'email@email.ru'
    password = '123123'
    username = 'testuser'

    def setUp(self):
        self.client = TestClient()

    def prepare_db(self):
        call_command('loaddata', 'user.yaml', verbosity=0)
        call_command('loaddata', 'client.yaml', verbosity=0)
        return User.objects.get(username=self.username)

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
