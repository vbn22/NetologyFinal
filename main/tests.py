# -*- coding: utf-8 -*-
import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.test import Client as TestClient
from django.core.management import call_command
from .models import Things, Subscriptions, Days
from datetime import datetime,timedelta
import json

'''
1. Тесты
- Насколко я понимаю, файлы .json в fixtures представляют из себя некий набор данных, который используется. Он задается в тестах, но нигде не используется. Я не очень понимаю, зачем это делать в тестах

    при запуске теста создается пустая тестовая база.
    чтобы не создавать там необходимые данные каждый раз используются фикстуры, они загружаются в базу автоматически при запуске теста
    например в классе CreateSubscriptionTest подгружаются данные о том какие товары можно заказать (things.json)
    это необходимо например при тестировании покупки одного товара test_buy_subscribe_with_one_thing

- Названия 'thing' в тестах не отражают нашей предметной области. Thing - нечто абстрактное, но мы-то продаем реальные станки и бритвы

    исправил, назвал тесты более развернуто

- Строчки типа period_type = Subscriptions.PERIOD_TYPE[0][0] не добавляют информативности тесту.

    к сожелению полностью уйти от [0][0] не удалось, вынес в get_id_period

- Названия тестов: test_subscribe_with_type_period. Что тестируем? Подписку? А что в итоге? Как понять, что проверяет тест? Я полагаю, что он проверяет успешность оформления подписки, но это лишь предположение, я не могу понять это из названия

    изменил название

2) Коммиты, CI. Тут все хорошо

3) Рефакторинг есть, его можно делать бесконечно )
'''


email = 'email@email.ru'
password = '123123'
username = 'testuser'
last_name = 'last_name'

class UserAuthTest(TestCase):
    fixtures = ['user.json','client.json']
    client,user = None,None

    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.get(username=username)

    def test_client_can_register(self):
        username2 = 'username2'
        email2 = 'test2@test.ru'
        data = dict(username=username2,
                    wallet=100,
                    last_name=last_name,
                    email=email2,
                    password1=password,
                    password2=password
                    )
        self.client.post('/register/',data)
        self.assertTrue(User.objects.filter(username=username2))

    def test_client_can_login(self):
        data = dict(username=username,password=password)
        self.client.post('/login/',data)
        self.assertTrue(get_user(self.client).is_authenticated())

    def test_client_can_logout(self):
        self.client.login(username=username, password=password)
        self.client.get('/logout/')
        self.assertTrue(get_user(self.client).is_anonymous())


class CreateSubscriptionTest(TestCase):
    fixtures = ['user.json','client.json','things.json','days.json']
    client,user = None,None

    def setUp(self,*args, **kwargs):
        self.client = TestClient()
        self.client.login(username=username, password=password)
        self.user = User.objects.get(username=username)

    def get_id_period(self,name_of_period):
        return filter(lambda x:x[1] == name_of_period,Subscriptions.PERIOD_TYPE)[0][0]

    def tearDown(self):
        Subscriptions.objects.all().delete()

    def test_when_client_buy_blade_then_blade_is_contained_in_subscription(self):
        products_in_cart = Things.objects.filter(title="Бритвенный станок").values_list('id',flat=True)
        self.client.post('/subscribe/buy', dict(things=products_in_cart))
        products_in_subscription = self.user.profile.subscriptions.all()[0].things.values_list('id',flat=True)
        self.assertEqual(set(products_in_cart),set(products_in_subscription))

    def test_when_client_buy_all_products_then_all_products_are_contained_in_subscription(self):
        products_in_cart = Things.objects.all().values_list('id',flat=True)
        self.client.post('/subscribe/buy', dict(things=products_in_cart))
        products_in_subscription = self.user.profile.subscriptions.all()[0].things.values_list('id',flat=True)
        self.assertEqual(set(products_in_cart),set(products_in_subscription))

    def test_when_client_select_once_a_month_then_subscription_period_is_once_a_month(self):
        period_type = self.get_id_period('Раз в месяц')
        self.client.post('/subscribe/buy', dict(period_type=period_type))
        subscription_period_type = self.user.profile.subscriptions.all()[0].period_type
        self.assertEqual(period_type,subscription_period_type)

    def test_when_client_select_1_and_3_day_then_these_days_contained_in_subscription(self):
        days_ids = Days.objects.filter(day__in=[1,3]).values_list('id',flat=True)
        self.client.post('/subscribe/buy', dict(days=days_ids))
        subscription_days_ids = self.user.profile.subscriptions.all()[0].days.values_list('id',flat=True)
        self.assertEqual(set(days_ids),set(subscription_days_ids))


class EditSubscriptionTest(TestCase):
    fixtures = ['user.json','client.json','things.json','days.json','subscriptions.json']
    client,user,subscription_id = None,None,None

    def setUp(self,*args, **kwargs):
        self.client = TestClient()
        self.client.login(username=username, password=password)
        self.user = User.objects.get(username=username)
        self.subscription_id = self.user.profile.subscriptions.all()[0].id

    def tearDown(self):
        Subscriptions.objects.all().delete()

    def test_client_can_open_page_with_list_of_subscriptions(self):
        response = self.client.get('/subscribe/list')
        self.assertTrue(response.context['subscriptions'])

    def test_client_can_open_page_edit_subscription(self):
        response = self.client.get('/subscribe/edit/'+str(self.subscription_id))
        self.assertTrue(response.context['subscribe_form'])

    def test_client_can_change_days_in_subscription(self):
        new_days_ids = Days.objects.filter(day__in=[2,25]).values_list('id',flat=True)
        self.client.post('/subscribe/edit/'+str(self.subscription_id),dict(days=new_days_ids))
        subscription_new_days_ids = self.user.profile.subscriptions.all()[0].days.values_list('id',flat=True)
        self.assertEqual(set(new_days_ids),set(subscription_new_days_ids))

    def test_client_can_stop_subscription(self):
        status = False
        self.client.post('/subscribe/edit/'+str(self.subscription_id),dict(status=status))
        subscription_status = self.user.profile.subscriptions.all()[0].status
        self.assertEqual(status,subscription_status)

    def test_client_can_remove_subscription(self):
        self.client.get('/subscribe/remove/'+str(self.subscription_id))
        self.assertFalse(self.user.profile.subscriptions.all())


class PriceTest(TestCase):
    fixtures = ['user.json','client.json','things.json','days.json','subscriptions.json']
    client,user,subscription,subscription_id = None,None,None,None

    '''
    предсозданная тестовая подписка от 2016-12-24:
    бритвенный станок (1$)
    гель для бритья (8$)
    два раза в месяц: 3 и 10 числа
    '''

    def setUp(self,*args, **kwargs):
        self.client = TestClient()
        self.client.login(username=username, password=password)
        self.user = User.objects.get(username=username)
        self.subscription = self.user.profile.subscriptions.all()[0]
        self.subscription_id = self.subscription.id

    def test_client_can_calculate_cost_for_date(self):
        date = datetime.strptime('01-02-2017','%d-%m-%Y')
        url = '/calculate/'+str(self.subscription_id)+'/'+date.strftime('%d-%m-%Y')
        self.assertEqual((1+8)+(1+8),int(self.client.get(url).context['result_calculate']))


    def test_client_can_get_list_of_subscription_dates(self):
        start_date = '01-01-2017'
        end_date = '01-02-2017'
        url = '/get_list_of_dates/%s/%s/%s'%(self.subscription_id,start_date,end_date)
        response = self.client.get(url)
        response = json.loads(response.content)
        list_of_dates = [u'01/03/2017',u'01/10/2017']
        self.assertEqual(set(list_of_dates),set(response['list_of_dates']))
