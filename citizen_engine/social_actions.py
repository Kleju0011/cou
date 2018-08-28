from citizen_engine.citizen_abstract import CitizenAbstract
from citizen_engine.models import Citizen
import random, string
from city_engine.models import Residential


class SocialAction:
    def __init__(self, city, profile, city_data):
        self.city = city
        self.profile = profile
        self.city_data = city_data
        self.citizen_data = CitizenAbstract(self.city, self.profile, self.city_data)

    def run(self):
        self.match_marriages()
        self.born_child()
        self.save_all()

    def save_all(self):
        for c in self.citizen_data.citizens_in_city:
            c.save()

    def find_place_to_live(self, m, f):
        if f.resident_object and m.resident_object:
            total_residents_in_m = m.resident_object.max_population - self.city_data.list_of_buildings[m.resident_object]['people_in_charge']
            total_residents_in_f = f.resident_object.max_population - self.city_data.list_of_buildings[f.resident_object]['people_in_charge']
            if total_residents_in_f > 0 and total_residents_in_m > 0:
                return random.choice([f.resident_object, m.resident_object])
            elif total_residents_in_m > 0 and total_residents_in_f == 0:
                return m.resident_object
            elif total_residents_in_f > 0 and total_residents_in_m == 0:
                return f.resident_object
        elif m.resident_object and \
                m.resident_object.max_population - self.city_data.list_of_buildings[m.resident_object]['people_in_charge'] > 0:
            return m.resident_object
        elif f.resident_object and \
                f.resident_object.max_population - self.city_data.list_of_buildings[f.resident_object]['people_in_charge'] > 0:
            return f.resident_object

    def match_marriages(self):
        males = [m for m in self.citizen_data.mature_males if m.partner_id == 0]
        if males is not None:
            females = [m for m in self.citizen_data.mature_females if m.partner_id == 0]
            random.shuffle(males)
            random.shuffle(females)
            for m, f in zip(males, females):
                if random.random() < self.citizen_data.chance_to_marriage[f.age] \
                        and random.random() < self.citizen_data.chance_to_marriage[m.age]\
                        and self.find_place_to_live(m, f) is not None:
                    place_to_live = self.find_place_to_live(m, f)
                    f.partner_id = m.id
                    m.partner_id = f.id
                    f.surname = m.surname
                    f.resident_object = place_to_live
                    m.resident_object = place_to_live
                    self.city_data.list_of_buildings[place_to_live]['people_in_charge'] += 1
        self.citizen_data.create_and_return_pairs_in_city()

    def check_if_there_is_place_for_child(self, ml):
        return ml.resident_object.max_population \
               - self.city_data.list_of_buildings[ml.resident_object]['people_in_charge'] > 0

    def born_child(self):
        for family in self.citizen_data.pairs_in_city:
            ml = self.citizen_data.pairs_in_city[family][Citizen.MALE]
            fl = self.citizen_data.pairs_in_city[family][Citizen.FEMALE]
            if random.random() < self.citizen_data.chance_to_born[ml.age] \
                    and random.random() < self.citizen_data.chance_to_born[fl.age] \
                    and self.check_if_there_is_place_for_child(ml):
                Citizen.objects.create(
                    city=self.city,
                    age=0,
                    month_of_birth=self.profile.current_turn,
                    cash=0,
                    health=5,
                    name="".join([random.choice(string.ascii_letters) for x in range(5)]),
                    surname=ml.surname,
                    sex=random.choice(Citizen.SEX)[0],
                    father_id=fl.id,
                    mother_id=ml.id,
                    resident_object=ml.resident_object
                )
                self.city_data.list_of_buildings[ml.resident_object]['people_in_charge'] += 1