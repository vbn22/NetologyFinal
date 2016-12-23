# -*- coding: utf-8 -*-
import unittest
from django.contrib.auth.models import User
from django.test import Client as TestClient


class BasicTest(unittest.TestCase):
    email = 'email@email.ru'
    password = '123123'

    def test_client_can_register(self):
        self.client = TestClient()
        data = dict(username='testuser',
                    wallet=100,
                    last_name='last_name',
                    email=self.email,
                    password1=self.password,
                    password2=self.password
                    )
        self.client.post('/register/',data)
        self.assertTrue(User.objects.filter(email=self.email))

