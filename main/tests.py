# -*- coding: utf-8 -*-
import unittest
from django.contrib.auth.models import User
from django.test import Client as TestClient


class BasicTest(unittest.TestCase):

    def test_client_can_register(self):
        self.client = TestClient()
        email = 'email@email.ru'
        data = dict(username='testuser',wallet=100,last_name='last_name',email=email)
        self.client.post('/register/',data)
        print User.objects.filter(email=email)
        self.assertTrue(User.objects.filter(email=email))

