# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True,related_name='profile')
    wallet = models.FloatField(default=100.0, verbose_name='wallet')


class Things(models.Model):
    title = models.CharField(verbose_name='Name',default='default',max_length=125)
    price = models.FloatField(default=1.0,verbose_name='price')

    def __unicode__(self):
        return self.title

class Days(models.Model):
    day = models.PositiveSmallIntegerField(default=1)

    def __unicode__(self):
        return str(self.day)

class Subscriptions(models.Model):
    PERIOD_TYPE = ((0, ('Раз в два месяца')),
                   (1, ('Раз в месяц')),
                   (2, ('Два раза в месяц'))
                   )

    user = models.ForeignKey(Client,verbose_name='user',related_name='subscriptions',blank=True,null=True)
    things = models.ManyToManyField(Things,verbose_name='things', blank=True)
    date_of_purchase = models.DateTimeField(auto_now=True)
    period_type = models.PositiveSmallIntegerField(choices=PERIOD_TYPE, default=0)
    days = models.ManyToManyField(Days,verbose_name='days',blank=True,null=True)
