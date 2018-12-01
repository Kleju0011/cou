from django.db import models
from city_engine.models import WindPlant, WaterTower, ProductionBuilding, City, Residential, DumpingGround, DustCart, BuldingsWithWorkes
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from city_engine.main_view_data.global_variables import ROW_NUM, HEX_NUM_IN_ROW
import random
from cou.global_var import TRAINEE, JUNIOR, MASTER, PROFESSIONAL, REGULAR,\
    MALE, FEMALE,\
    ELEMENTARY, COLLEGE, PHD


class Family(models.Model):
    surname = models.CharField(default='', max_length=30)
    city = models.ForeignKey(City)


class Citizen(models.Model):
    EDUCATION = (
        (ELEMENTARY, 'Elementary'),
        (COLLEGE, 'College'),
        (PHD, 'PhD')
    )

    SEX = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    city = models.ForeignKey(City)
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    family = models.ForeignKey(Family, null=True)
    age = models.IntegerField()
    month_of_birth = models.IntegerField()
    sex = models.CharField(choices=SEX, max_length=5)
    edu_title = models.CharField(choices=EDUCATION, max_length=10, default='None')
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    health = models.IntegerField()

    partner_id = models.PositiveIntegerField(default=0)
    father_id = models.PositiveIntegerField(default=0)
    mother_id = models.PositiveIntegerField(default=0)

    workplace_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True,
                                               related_name='workplace_place')
    workplace_object_id = models.PositiveIntegerField(null=True)
    workplace_object = GenericForeignKey('workplace_content_type', 'workplace_object_id')

    resident_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True,
                                              related_name='resident_place')
    resident_object_id = models.PositiveIntegerField(null=True)
    resident_object = GenericForeignKey('resident_content_type', 'resident_object_id')

    school_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True,
                                            related_name='school_place')
    school_object_id = models.PositiveIntegerField(null=True)
    school_object = GenericForeignKey('school_content_type', 'school_object_id')

    def change_work_for_better(self, workplaces, citizens, save_instance):
        matrix = {ELEMENTARY: 'elementary_vacancies', COLLEGE: 'college_vacancies', PHD: 'phd_vacancies', 'None': 'elementary_vacancies'}
        possible_workplaces, edu_level = self.__possible_workplaces(workplaces)
        if possible_workplaces:
            current_profession = citizens[self].current_profession
            setattr(workplaces[self.workplace_object], matrix[edu_level], getattr(workplaces[self.workplace_object], matrix[edu_level]) - 1)
            current_profession.if_current = False

            best = self.__find_better_work_option(possible_workplaces)
            setattr(workplaces[best], matrix[edu_level], getattr(workplaces[best], matrix[edu_level]) + 1)
            self.workplace_object = best
            citizens[self].current_profession = Profession.objects.create(
                citizen=self, name=best.profession_type_provided, education=edu_level)
            save_instance.append(citizens[self].current_profession)

    def find_work(self, workplaces, citizens, save_instance):
        matrix = {ELEMENTARY: 'elementary_vacancies', COLLEGE: 'college_vacancies', PHD: 'phd_vacancies', 'None': 'elementary_vacancies'}
        possible_workplaces, edu_level = self.__possible_workplaces(workplaces)
        if possible_workplaces:
            best = self.__find_better_work_option(possible_workplaces)
            self.workplace_object = best
            setattr(workplaces[best], matrix[edu_level], getattr(workplaces[best], matrix[edu_level]) + 1)
            citizens[self].current_profession = Profession.objects.create(
                citizen=self, name=best.profession_type_provided, education=edu_level)
            save_instance.append(citizens[self].current_profession)
            save_instance.append(self)

    def __possible_workplaces(self, workplaces):
        matrix = {ELEMENTARY: 'elementary_vacancies', COLLEGE: 'college_vacancies', PHD: 'phd_vacancies', 'None': 'elementary_vacancies'}
        if [w for w in workplaces if getattr(workplaces[w], matrix[self.edu_title])]:
            return [w for w in workplaces if getattr(workplaces[w], matrix[self.edu_title])], self.edu_title
        else:
            education_levels = [e[0] for e in Profession.EDUCATION]
            current_education_level = education_levels.index(self.edu_title)
            if current_education_level > 0:
                while current_education_level:
                    current_education_level -= 1
                    new_education_level = education_levels[current_education_level]
                    return [w for w in workplaces if getattr(workplaces[w], matrix[new_education_level])], new_education_level

    def __find_better_work_option(self, workplaces):
        col = self.resident_object.city_field.col
        row = self.resident_object.city_field.row
        pattern = sorted(workplaces, key=lambda x: (
            abs(x.city_field.col - col), abs(x.city_field.row - row)) if isinstance(x, BuldingsWithWorkes)
        else (random.randrange(HEX_NUM_IN_ROW), random.randrange(ROW_NUM)))
        chances = {len(pattern)/x: y for x, y in enumerate(pattern, start=1)}
        return chances[sorted(chances.keys()).pop()]

    def __str__(self):
        return "{} {}".format(self.name, self.surname)


class Profession(models.Model):
    EDUCATION = (
        (ELEMENTARY, 'Elementary'),
        (COLLEGE, 'College'),
        (PHD, 'PhD')
    )
    JOB_GRADES = (
        (TRAINEE, "Trainee"),
        (JUNIOR, "Junior"),
        (REGULAR, "Regular"),
        (PROFESSIONAL, "Professional"),
        (MASTER, "Master")
    )
    job_grade_info = {job_grade[0]: {'divisor': divisor, 'border': border} for job_grade, divisor, border in zip(
        JOB_GRADES, (50, 40, 190, 120, 480), (0.10, 0.40, 0.60, 1, 1.30)
    )}
    citizen = models.ForeignKey(Citizen)
    name = models.CharField(default='', max_length=30)
    job_grade = models.CharField(choices=JOB_GRADES, max_length=15, default=TRAINEE)
    education = models.CharField(choices=EDUCATION, max_length=10, default='None')
    proficiency = models.FloatField(default=0)
    if_current = models.BooleanField(default=True)

    def __proficiency_divisor(self):
        return Profession.job_grade_info[self.job_grade]['divisor']

    def __check_job_grade(self):
        if self.proficiency > Profession.job_grade_info[self.job_grade]['border']:
            cur_level_index = [job_grade[0] for job_grade in Profession.JOB_GRADES].index(self.job_grade)
            try:
                self.job_grade = Profession.JOB_GRADES[cur_level_index + 1][0]
            except IndexError:
                self.job_grade = Profession.JOB_GRADES[-1][0]

    def update_proficiency(self, citizens_in_city):
        citizen = citizens_in_city[self.citizen]
        citizen_education = [e.effectiveness for e in citizen.educations]
        citizen.current_profession.proficiency += (sum(citizen_education)/len(citizen_education))/self.__proficiency_divisor()
        self.__check_job_grade()


class Education(models.Model):
    EDUCATION = (
        (ELEMENTARY, 'Elementary'),
        (COLLEGE, 'College'),
        (PHD, 'PhD')
    )
    citizen = models.ForeignKey(Citizen)
    name = models.CharField(choices=EDUCATION, max_length=15)
    effectiveness = models.FloatField(default=0.00)
    if_current = models.BooleanField(default=True)
    cur_year_of_learning = models.PositiveIntegerField(default=0)
    max_year_of_learning = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
