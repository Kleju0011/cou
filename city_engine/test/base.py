from django.test import TestCase
from django.contrib.auth.models import User
from city_engine.main_view_data.board import Board
from citizen_engine.models import Citizen
from city_engine.models import City, CityField, \
    Residential, \
    ProductionBuilding, \
    WindPlant, CoalPlant, RopePlant, \
    WaterTower, \
    electricity_buildings, waterworks_buildings, \
    list_of_models


class CityFixture(TestCase):
    def setUp(self):
        first_user = User.objects.create_user(username='test_username', password='12345', email='random@wp.pl')
        self.client.login(username='test_username', password='12345', email='random@wp.pl')
        first_city = City.objects.create(name='Wrocław', user=first_user, cash=10000)

        second_user = User.objects.create_user(username='test_username_2', password='54321', email='random2@wp.pl')
        second_city = City.objects.create(name='Łódź', user=second_user, cash=10000)

        for field_id in range(1, int(Board.HEX_NUM) + 1):
            CityField.objects.create(city=first_city, field_id=field_id).save()
            CityField.objects.create(city=second_city, field_id=field_id).save()

        CityField.objects.get(field_id=1, city=first_city).if_production = True
        CityField.objects.get(field_id=2, city=first_city).if_residential = True
        CityField.objects.get(field_id=3, city=first_city).if_electricity = True
        CityField.objects.get(field_id=1, city=first_city).save()
        CityField.objects.get(field_id=2, city=first_city).save()
        CityField.objects.get(field_id=3, city=first_city).save()

        CityField.objects.get(field_id=1, city=second_city).if_production = True
        CityField.objects.get(field_id=2, city=second_city).if_residential = True
        CityField.objects.get(field_id=3, city=second_city).if_electricity = True
        CityField.objects.get(field_id=1, city=second_city).save()
        CityField.objects.get(field_id=2, city=second_city).save()
        CityField.objects.get(field_id=3, city=second_city).save()

        first_factory = ProductionBuilding()
        first_factory.max_employees = 20
        first_factory.current_employees = 0
        first_factory.production_level = 0
        first_factory.build_time = 3
        first_factory.city = first_city
        first_factory.if_under_construction = False
        first_factory.city_field = CityField.objects.get(field_id=1, city=first_city)
        first_factory.save()

        second_factory = ProductionBuilding()
        second_factory.max_employees = 20
        second_factory.current_employees = 0
        second_factory.production_level = 0
        second_factory.build_time = 3
        second_factory.city = second_city
        second_factory.if_under_construction = False
        second_factory.city_field = CityField.objects.get(field_id=1, city=second_city)
        second_factory.save()

        first_residential = Residential()
        first_residential.max_population = 20
        first_residential.current_population = 4
        first_residential.residential_level = 0
        first_residential.build_time = 3
        first_residential.city = first_city
        first_residential.if_under_construction = False
        first_residential.city_field = CityField.objects.get(field_id=2, city=first_city)
        first_residential.save()

        second_residential = Residential()
        second_residential.max_population = 20
        second_residential.current_population = 4
        second_residential.residential_level = 0
        second_residential.build_time = 3
        second_residential.city = second_city
        second_residential.if_under_construction = False
        second_residential.city_field = CityField.objects.get(field_id=2, city=second_city)
        second_residential.save()

        first_power_plant = WindPlant()
        first_power_plant.max_employees = 5
        first_power_plant.current_employees = 2
        first_power_plant.build_time = 3
        first_power_plant.power_nodes = 1
        first_power_plant.max_power_nodes = 10
        first_power_plant.energy_production = 5
        first_power_plant.city = first_city
        first_power_plant.if_under_construction = True
        first_power_plant.city_field = CityField.objects.get(field_id=3, city=first_city)
        first_power_plant.save()

        second_power_plant = WindPlant()
        second_power_plant.max_employees = 10
        second_power_plant.current_employees = 3
        second_power_plant.build_time = 3
        second_power_plant.power_nodes = 1
        second_power_plant.max_power_nodes = 10
        second_power_plant.energy_production = 5
        second_power_plant.city = second_city
        second_power_plant.if_under_construction = False
        second_power_plant.city_field = CityField.objects.get(field_id=3, city=second_city)
        second_power_plant.save()

        third_power_plant = RopePlant()
        third_power_plant.max_employees = 10
        third_power_plant.current_employees = 3
        third_power_plant.build_time = 4
        third_power_plant.power_nodes = 1
        third_power_plant.max_power_nodes = 4
        third_power_plant.energy_production = 30
        third_power_plant.city = first_city
        third_power_plant.if_under_construction = False
        third_power_plant.city_field = CityField.objects.get(field_id=4, city=first_city)
        third_power_plant.save()

        fourth_power_plant = CoalPlant()
        fourth_power_plant.max_employees = 15
        fourth_power_plant.current_employees = 3
        fourth_power_plant.build_time = 5
        fourth_power_plant.power_nodes = 1
        fourth_power_plant.max_power_nodes = 4
        fourth_power_plant.energy_production = 30
        fourth_power_plant.city = first_city
        fourth_power_plant.if_under_construction = False
        fourth_power_plant.city_field = CityField.objects.get(field_id=5, city=first_city)
        fourth_power_plant.save()

        waterwork = WaterTower()
        waterwork.max_employees = 5
        waterwork.current_employees = 3
        waterwork.build_time = 1
        waterwork.water_production = 20
        waterwork.city = first_city
        waterwork.if_under_construction = False
        waterwork.city_field = CityField.objects.get(field_id=6, city=first_city)
        waterwork.save()

        first_citizen = Citizen()
        first_citizen.age = 22
        first_citizen.health = 20
        first_citizen.city = first_city
        first_citizen.income = 100
        first_citizen.residential = first_residential
        first_citizen.production_building = first_factory
        first_citizen.save()

        second_citizen = Citizen()
        second_citizen.age = 60
        second_citizen.health = 10
        second_citizen.city = first_city
        second_citizen.income = 100
        second_citizen.residential = first_residential
        second_citizen.production_building = first_factory
        second_citizen.save()

        third_citizen = Citizen()
        third_citizen.age = 40
        third_citizen.health = 25
        third_citizen.income = 10
        third_citizen.city = first_city
        third_citizen.residential = first_residential
        third_citizen.production_building = first_factory
        third_citizen.save()