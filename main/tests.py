# -*- coding: utf-8 -*-
import unittest
from django.contrib.auth.models import User
from django.test import Client as TestClient


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
