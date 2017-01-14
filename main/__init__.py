# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta


def diff_month(d1, d2):
    return (d1.year - d2.year)*12 + d1.month - d2.month


def get_dates(id,start_date,end_date):
    from .models import Subscriptions
    list_of_dates = []
    subscription = Subscriptions.objects.get(pk=id)
    month_shift = 0
    while True:
        for item_day in subscription.days.all():
            day = item_day.day
            while True:
                try:
                    date = start_date.replace(day=day) + relativedelta(months=month_shift)
                    if date in list_of_dates:
                        raise ValueError('Date already exists')
                    list_of_dates.append(date)
                    break
                except ValueError:
                    day += 1
        month_shift += 1
        if list_of_dates and list_of_dates[-1] > end_date:
            break
    list_of_dates = filter(lambda day:day <= end_date and day > start_date,list_of_dates)
    return list_of_dates