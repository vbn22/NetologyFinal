# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True,related_name='profile')
    wallet = models.FloatField(default=100.0, verbose_name='price')
