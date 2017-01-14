# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta


def diff_month(d1, d2):
    return (d1.year - d2.year)*12 + d1.month - d2.month


def get_day(day,month_shift,start_date,list_of_dates):
    while True:
        try:
            date = start_date.replace(day=day) + relativedelta(months=month_shift)
            if date in list_of_dates:
                raise ValueError('Date already exists')
            return date
        except ValueError:
            day += 1


def get_month_shift(subscription):
    return 2 if subscription.period_type == 0 else 1


def get_dates(id,start_date,end_date):
    from .models import Subscriptions
    list_of_dates = []
    month_shift = 0
    subscription = Subscriptions.objects.get(pk=id)
    if not subscription.status:
        return list_of_dates
    while True:
        for item_day in subscription.days.all():
            list_of_dates.append(get_day(item_day.day,month_shift,start_date,list_of_dates))
        month_shift += get_month_shift(subscription)
        if max(list_of_dates) > end_date:
            break
    list_of_dates = filter(lambda day:day <= end_date and day > start_date,list_of_dates)
    return list_of_dates