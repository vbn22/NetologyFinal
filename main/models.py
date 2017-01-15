# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.dispatch import receiver



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True,related_name='profile')
    wallet = models.FloatField(default=100.0, verbose_name='wallet')

    @property
    def get_wallet(self):
        return self.wallet - sum([x.calculate(datetime.now()) for x in self.subscriptions.all()])


class Things(models.Model):
    title = models.CharField(verbose_name='Name',default='default',max_length=125)
    price = models.FloatField(default=1.0,verbose_name='price')

    def __unicode__(self):
        return '%s (%s$)'%(self.title,self.price)

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
    status = models.BooleanField(default=True,verbose_name='Status')

    def calculate(self,date):
        from main import get_dates
        result_calculate = 0
        for day in get_dates(self.id,self.date_of_purchase.replace(tzinfo=None),date):
            result_calculate += sum(self.things.values_list('price',flat=True))
        return result_calculate