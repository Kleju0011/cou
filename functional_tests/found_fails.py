from django.contrib.auth.models import User
from django.test import override_settings
from selenium import webdriver

from citizen_engine.models import Citizen, Family, Profession
from city_engine.models import (
    City,
    Field,
    StandardLevelResidentialZone,
    WaterTower,
    WindPlant,
    SewageWorks,
)
from cou.abstract import RootClass
from cou.global_var import FEMALE, MALE, ELEMENTARY
from functional_tests.page_objects import MainView, LoginPage, Homepage
from resources.models import Market
from .legacy.base import BaseTest
import time


@override_settings(DEBUG=True)
class CitizenBasicTests(BaseTest):
    fixtures = ["basic_basic_fixture.json"]

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.city = City.objects.latest("id")
        self.user = User.objects.latest("id")
        self.browser.implicitly_wait(3)
        self.market = Market.objects.create(profile=self.user.profile)

    def test_born_child_failed(self):
        field = list(Field.objects.all())
        s = StandardLevelResidentialZone.objects.create(
            city=self.city, if_under_construction=False, city_field=field.pop()
        )
        s.self__init(2)
        s.save()
        family = Family.objects.create(city=self.city, surname="01")
        self.f = Citizen.objects.create(
            city=self.city,
            age=21,
            month_of_birth=2,
            cash=400,
            health=5,
            name="AnonKA",
            surname="FeSurname",
            sex=FEMALE,
            resident_object=s,
            family=family,
        )
        self.m = Citizen.objects.create(
            city=self.city,
            age=21,
            month_of_birth=2,
            cash=400,
            health=5,
            name="AnON",
            surname="MaSurname",
            sex=MALE,
            resident_object=s,
            family=family,
        )
        self.f.partner_id = self.m.id
        self.m.partner_id = self.f.id
        self.m.save()
        self.f.save()
        self.assertEqual(self.f.partner_id, self.m.id)
        self.assertEqual(self.m.partner_id, self.f.id)
        self.assertEqual(self.m.resident_object, s)
        self.assertEqual(self.f.resident_object, s)
        homepage = Homepage(self.browser, self.live_server_url)
        homepage.navigate("/main/")
        self.assertIn("Login", self.browser.title)
        login_page = LoginPage(self.browser, self.live_server_url)
        login_page.login(username=self.user.username, password="test#123")
        self.assertTrue(User.objects.latest("id").is_authenticated)
        self.assertIn("Miasto {}".format(self.city.name), self.browser.title)
        main_view = MainView(self.browser, self.live_server_url)
        self.user.profile.if_social_enabled = True
        self.user.profile.chance_to_born_baby_percent = 1.00
        self.user.profile.save()
        self.assertEqual(self.user.profile.chance_to_born_baby_percent, 1.00)
        self.assertTrue(self.user.profile.if_social_enabled)
        self.assertEqual(s.max_population, 2)
        self.assertEqual(Citizen.objects.count(), 2)
        self.assertEqual(Family.objects.all().count(), 1)
        main_view.next_turns(5)

#
# @override_settings(DEBUG=True)
# class ResourcesTests(BaseTest):
#     fixtures = ["basic_basic_fixture.json"]
#
#     def setUp(self):
#         self.browser = webdriver.Chrome()
#         self.city = City.objects.latest("id")
#         self.user = User.objects.latest("id")
#         self.browser.implicitly_wait(3)
#         self.market = Market.objects.create(profile=self.user.profile)
#
#     def test_maximum_employees_per_building(self):
#         from random import choice, randrange
#         from citizen_engine.models import Education
#         import names
#
#         sex = choice(Citizen.SEX)[0]
#         surname = names.get_last_name()
#         f = Family.objects.create(surname=surname, city=self.city)
#         spec = Citizen.objects.create(
#             city=self.city,
#             age=randrange(18, 24),
#             name=names.get_first_name(sex.lower()),
#             surname=surname,
#             health=10,
#             month_of_birth=randrange(1, 12),
#             sex=sex,
#             family=f,
#             cash=500,
#         )
#
#         for x in range(12):
#             sex = choice(Citizen.SEX)[0]
#             surname = names.get_last_name()
#             f = Family.objects.create(surname=surname, city=self.city)
#             c = Citizen.objects.create(
#                 city=self.city,
#                 age=randrange(18, 24),
#                 name=names.get_first_name(sex.lower()),
#                 surname=surname,
#                 health=10,
#                 month_of_birth=randrange(1, 12),
#                 sex=sex,
#                 family=f,
#                 cash=500,
#                 edu_title=ELEMENTARY,
#             )
#             Education.objects.create(citizen=c, name=ELEMENTARY, effectiveness=0.50)
#
#         field = list(Field.objects.all())
#         s = StandardLevelResidentialZone.objects.create(
#             city=self.city, if_under_construction=False, city_field=field.pop()
#         )
#         s.self__init(13)
#         s.save()
#         self.city.save()
#         self.user.profile.if_social_enabled = True
#         self.user.profile.save()
#         homepage = Homepage(self.browser, self.live_server_url)
#         homepage.navigate("/main/")
#         self.assertIn("Login", self.browser.title)
#         login_page = LoginPage(self.browser, self.live_server_url)
#         login_page.login(username=self.user.username, password="test#123")
#         self.assertTrue(User.objects.latest("id").is_authenticated)
#         self.assertIn("Miasto {}".format(self.city.name), self.browser.title)
#         main_view = MainView(self.browser, self.live_server_url)
#         SewageWorks.objects.create(city_field=Field.objects.get(id=4957), city=self.city)
#         WaterTower.objects.create(city_field=Field.objects.get(id=4891), city=self.city)
#         WindPlant.objects.create(city_field=Field.objects.get(id=4828), city=self.city)
#
#         for x in range(7):
#             if WindPlant.objects.latest("id").if_under_construction is True:
#                 self.assertEqual(
#                     WindPlant.objects.latest("id").employee.all().count(), 0
#                 )
#             if WaterTower.objects.latest("id").if_under_construction is True:
#                 self.assertEqual(
#                     WaterTower.objects.latest("id").employee.all().count(), 0
#                 )
#             if SewageWorks.objects.latest("id").if_under_construction is True:
#                 self.assertEqual(
#                     SewageWorks.objects.latest("id").employee.all().count(), 0
#                 )
#             main_view.next_turn()
#         w = WindPlant.objects.latest("id")
#         s = SewageWorks.objects.latest("id")
#         wt = WaterTower.objects.latest("id")
#         self.assertEqual(
#             Profession.objects.all().count(), Citizen.objects.all().count()
#         )
#         rc = RootClass(self.city, User.objects.latest("id"))
#         self.assertEqual(
#             len(rc.list_of_workplaces[w].all_employees), w.employee.all().count()
#         )
#         self.assertEqual(
#             len(rc.list_of_workplaces[s].all_employees), s.employee.all().count()
#         )
#         self.assertEqual(
#             len(rc.list_of_workplaces[wt].all_employees), wt.employee.all().count()
#         )
        # self.assertGreater(w.energy_allocated, 20)
        # self.assertGreater(wt.raw_water_allocated, 50)
        # self.assertGreater(s.clean_water_allocated, 20)

        # Pokryj None education z testami jednostkowymi
        # Pokombinuj z wymaganiami odnosnie wody i pradu aby mozna bylo jako wystartowac
        # Zaimplementuj patent z oczyszczona oraz brudna woda
