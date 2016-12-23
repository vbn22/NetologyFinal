# -*- coding: utf-8 -*-
import unittest
from django.contrib.auth.models import User
from django.test import Client as TestClient
from django.core.management import call_command

class UserAuthTest(unittest.TestCase):
    email = 'email@email.ru'
    password = '123123'

    def setUp(self):
        self.client = TestClient()

    def test_client_can_register(self):
        data = dict(username='testuser',
                    wallet=100,
                    last_name='last_name',
                    email=self.email,
                    password1=self.password,
                    password2=self.password
                    )
        self.client.post('/register/',data)
        self.assertTrue(User.objects.filter(email=self.email))

    def test_login_client(self):
        call_command('loaddata', 'user.yaml', verbosity=0)
        call_command('loaddata', 'client.yaml', verbosity=0)
        data = dict(email=self.email,password=self.password)
        self.client.post('/login/',data)
        self.assertIn('_auth_user_id', self.client.session)
