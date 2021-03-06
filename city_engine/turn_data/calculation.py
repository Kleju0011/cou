from citizen_engine.social_actions import SocialAction
from city_engine.main_view_data.resources_allocation import ResourceAllocation
from city_engine.main_view_data.trash_management import TrashManagement, CollectGarbage
from city_engine.models import Farm, AnimalFarm, MedicalEstablishment, Prison
from resources.models import MassConventer
from .fire_strategy import FireStrategy
from .police_strategy import PoliceStrategy


class TurnCalculation:
    def __init__(self, city, data, profile, fire_strategy=FireStrategy, police_strategy=PoliceStrategy):
        self.city = city
        self.data = data
        self.profile = profile
        self.fire_strategy = fire_strategy(self.data)
        self.police_strategy = police_strategy(self.data)

    def run(self):
        SocialAction(self.city, self.profile, self.data).run()
        ResourceAllocation(self.city, self.data).run()
        self.fire_strategy.calculate_probability_of_fire_among_the_all_buildings()
        self.fire_strategy.simulate_fire_in_the_city()
        self.police_strategy.apply_crime_prevention_in_city()
        self.police_strategy.calculate_criminals_vs_police_in_city()
        self.health_of_population_action()
        self.health_care_actions()
        self.prisons_actions()
        TrashManagement(self.data).run()
        CollectGarbage(self.city, self.data).run()
        self.financial_actions()
        self.collect_mass()
        self.execute_maintenance()
        self.update_build_status()
        self.update_harvest_status()
        self.update_breeding_status()
        self.trade_district_actions()
        self.save_all()

    def prisons_actions(self):
        for p in (p for p in self.data.list_of_buildings.values() if isinstance(p.instance, Prison)):
            p.conduct_rehabilitation()

    def health_care_actions(self):
        for h in (b for b in self.data.list_of_buildings.values() if isinstance(b.instance, MedicalEstablishment)):
            h.work(self.data.list_of_buildings)

    def health_of_population_action(self):
        for c in self.data.citizens_in_city.values():
            c.probability_of_being_sick()

    def save_all(self):
        self.city.save()
        self.data.market.save_all()
        for instance in self.data.to_save:
            instance.save()
        for company in self.data.companies:
            self.data.companies[company].save_all()
        self.profile.current_turn += 1
        self.profile.save()

    def financial_actions(self):
        for f in self.data.families:
            self.data.families[f].pay_rent(self.city, self.profile)

    def trade_district_actions(self):
        for c in self.data.companies.values():
            c.create_goods()

    def collect_mass(self):
        for mass_collector in [
            mc for mc in self.data.list_of_buildings if isinstance(mc, MassConventer)
        ]:
            mass_collector.product_mass(self.data)

    def update_breeding_status(self):
        for farm in [
            b for b in self.data.list_of_buildings if isinstance(b, AnimalFarm)
        ]:
            farm.farm_operation(self.data)
            if self.data.list_of_buildings[farm].cattle:
                self.data.to_save.append(self.data.list_of_buildings[farm].cattle)

    def update_harvest_status(self):
        for farm in [b for b in self.data.list_of_buildings if isinstance(b, Farm)]:
            farm.update_harvest(self.profile.current_turn, self.data)

    def update_build_status(self):
        for building in self.data.list_of_buildings:
            if building.if_under_construction is True:
                building.build_status()

    def calculate_maintenance_cost(self):
        return sum([b.maintenance_cost for b in self.data.list_of_buildings])

    def execute_maintenance(self):
        self.city.cash - self.calculate_maintenance_cost()
