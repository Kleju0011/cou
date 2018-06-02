from django import test
from city_engine.test.base import TestHelper
from city_engine.models import CityField, Residential, City, WindPlant, WaterTower, \
    ProductionBuilding, DustCart, DumpingGround
from django.db.models import Sum
from citizen_engine.models import Citizen
from city_engine.main_view_data.employee_allocation import EmployeeAllocation
from city_engine.abstract import RootClass


class EmployeeAllocationTest(test.TestCase, TestHelper):
    fixtures = ['basic_fixture_resources_and_employees.json']

    def setUp(self):
        self.city = City.objects.latest('id')
        self.RC = RootClass(self.city)
        self.EA = EmployeeAllocation(city=self.city, data=self.RC)

    def test_not_full_production_buildings(self):
        self.assertIn(self.EA.not_full_production_buildings(), [WindPlant.objects.get(id=1), WindPlant.objects.get(id=2)
                                                                , WaterTower.objects.get(id=1), WaterTower.objects.get(id=2)])

        self.populate_city()

        self.assertEqual(self.EA.not_full_production_buildings(), None)

    def test_update_employee_allocation(self):
        self.assertEqual(sum([wp.employee.count() for wp in WindPlant.objects.filter(city=self.city)]), 0)
        self.assertEqual(sum([wt.employee.count() for wt in WaterTower.objects.filter(city=self.city)]), 0)
        self.assertEqual(sum([pb.employee.count() for pb in ProductionBuilding.objects.filter(city=self.city)]), 0)

        self.populate_city()

        self.assertEqual(sum([wp.employee.count() for wp in WindPlant.objects.filter(city=self.city)]), 10)
        self.assertEqual(sum([wt.employee.count() for wt in WaterTower.objects.filter(city=self.city)]), 10)

    def test_update_population(self):
        self.assertEqual(Citizen.objects.filter(city=self.city).count(), 0)
        self.EA.run()
        self.assertIn(Citizen.objects.filter(city=self.city).count(), [x for x in range(21)])

    def test_employee_to_vehicle_allocation(self):
        city_field_one = CityField.objects.get(id=1)
        city_field_two = CityField.objects.get(id=2)
        residential = Residential.objects.create(city=self.city, if_under_construction=False, city_field=city_field_two)
        dumping_ground = DumpingGround.objects.create(city=self.city, if_under_construction=False, city_field=city_field_one)
        dust_cart = DustCart.objects.create(city=self.city, dumping_ground=dumping_ground)
        self.assertEqual(dust_cart.employee.count(), 0)
        self.populate_city()
        dust_cart = DustCart.objects.latest('id')
        self.assertEqual(dust_cart.employee.count(), 3)