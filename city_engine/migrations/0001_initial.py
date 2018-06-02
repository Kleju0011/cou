# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-01 13:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField(default=60)),
                ('object_id', models.PositiveIntegerField()),
                ('name', models.CharField(default='Fasola', max_length=10)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BeanFarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('pollution_rate', models.FloatField(default=0.0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('max_employees', models.PositiveIntegerField(default=0)),
                ('build_time', models.PositiveIntegerField(default=1)),
                ('build_cost', models.PositiveIntegerField(default=200)),
                ('maintenance_cost', models.PositiveIntegerField(default=20)),
                ('energy_required', models.PositiveIntegerField(default=20)),
                ('water_required', models.PositiveIntegerField(default=40)),
                ('crops', models.PositiveIntegerField(default=0)),
                ('harvest', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='Farma fasoli', max_length=15)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=15, unique=True)),
                ('cash', models.DecimalField(decimal_places=2, default=10000, max_digits=20)),
                ('publish', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CityField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('col', models.PositiveIntegerField()),
                ('row', models.PositiveIntegerField()),
                ('pollution', models.PositiveIntegerField(default=0)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
            ],
        ),
        migrations.CreateModel(
            name='CoalPlant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('energy_required', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('water_required', models.PositiveIntegerField(default=0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('max_employees', models.PositiveIntegerField(default=0)),
                ('power_nodes', models.PositiveIntegerField(default=0)),
                ('max_power_nodes', models.PositiveIntegerField(default=1)),
                ('energy_production', models.PositiveIntegerField(default=0)),
                ('energy_allocated', models.PositiveIntegerField(default=0)),
                ('if_electricity', models.BooleanField(default=True)),
                ('name', models.CharField(default='Elektrownia węglowa', max_length=20)),
                ('build_time', models.PositiveIntegerField(default=4)),
                ('build_cost', models.PositiveIntegerField(default=150)),
                ('maintenance_cost', models.PositiveIntegerField(default=15)),
                ('pollution_rate', models.FloatField(default=1.5)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
                ('city_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DumpingGround',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('water_required', models.PositiveIntegerField(default=0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('max_employees', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='Wysypisko śmieci', max_length=20)),
                ('if_dumping_ground', models.BooleanField(default=True)),
                ('build_time', models.PositiveIntegerField(default=2)),
                ('build_cost', models.PositiveIntegerField(default=100)),
                ('maintenance_cost', models.PositiveIntegerField(default=10)),
                ('energy_required', models.PositiveIntegerField(default=1)),
                ('limit_of_dust_cars', models.PositiveIntegerField(default=6)),
                ('current_space_for_trash', models.PositiveIntegerField(default=0)),
                ('max_space_for_trash', models.PositiveIntegerField(default=10000)),
                ('pollution_rate', models.FloatField(default=3.0)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
                ('city_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DustCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_cos', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='Śmieciarka', max_length=20)),
                ('cost', models.PositiveIntegerField(default=10)),
                ('max_employees', models.PositiveIntegerField(default=3)),
                ('curr_capacity', models.PositiveIntegerField(default=0)),
                ('max_capacity', models.PositiveIntegerField(default=60)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='city_engine.City')),
                ('dumping_ground', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='city_engine.DumpingGround')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lettuce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField(default=60)),
                ('object_id', models.PositiveIntegerField()),
                ('name', models.CharField(default='Sałata', max_length=10)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LettuceFarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('pollution_rate', models.FloatField(default=0.0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('max_employees', models.PositiveIntegerField(default=0)),
                ('build_time', models.PositiveIntegerField(default=1)),
                ('build_cost', models.PositiveIntegerField(default=200)),
                ('maintenance_cost', models.PositiveIntegerField(default=20)),
                ('energy_required', models.PositiveIntegerField(default=20)),
                ('water_required', models.PositiveIntegerField(default=40)),
                ('crops', models.PositiveIntegerField(default=0)),
                ('harvest', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='Farma sałaty', max_length=15)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
                ('city_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Potato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField(default=60)),
                ('object_id', models.PositiveIntegerField()),
                ('name', models.CharField(default='Ziemniaki', max_length=10)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PotatoFarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('pollution_rate', models.FloatField(default=0.0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('max_employees', models.PositiveIntegerField(default=0)),
                ('build_time', models.PositiveIntegerField(default=1)),
                ('build_cost', models.PositiveIntegerField(default=200)),
                ('maintenance_cost', models.PositiveIntegerField(default=20)),
                ('energy_required', models.PositiveIntegerField(default=20)),
                ('water_required', models.PositiveIntegerField(default=40)),
                ('crops', models.PositiveIntegerField(default=0)),
                ('harvest', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='Farma ziemniaków', max_length=20)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
                ('city_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductionBuilding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('energy_required', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('water_required', models.PositiveIntegerField(default=0)),
                ('pollution_rate', models.FloatField(default=0.0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='Budynek Przemysłowy', max_length=20)),
                ('if_production', models.BooleanField(default=True)),
                ('build_time', models.PositiveIntegerField(default=1)),
                ('build_cost', models.PositiveIntegerField(default=100)),
                ('maintenance_cost', models.PositiveIntegerField(default=10)),
                ('max_employees', models.PositiveIntegerField(default=20)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
                ('city_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Residential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('pollution_rate', models.FloatField(default=0.0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='Budynek Mieszkalny', max_length=20)),
                ('population', models.PositiveIntegerField(default=0)),
                ('max_population', models.PositiveIntegerField(default=30)),
                ('if_residential', models.BooleanField(default=True)),
                ('build_time', models.PositiveIntegerField(default=1)),
                ('build_cost', models.PositiveIntegerField(default=100)),
                ('maintenance_cost', models.PositiveIntegerField(default=10)),
                ('water_required', models.PositiveIntegerField(default=5)),
                ('energy_required', models.PositiveIntegerField(default=5)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
                ('city_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RopePlant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('energy_required', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('max_employees', models.PositiveIntegerField(default=0)),
                ('power_nodes', models.PositiveIntegerField(default=0)),
                ('max_power_nodes', models.PositiveIntegerField(default=1)),
                ('energy_production', models.PositiveIntegerField(default=0)),
                ('energy_allocated', models.PositiveIntegerField(default=0)),
                ('if_electricity', models.BooleanField(default=True)),
                ('name', models.CharField(default='Elektrownia na ropę', max_length=20)),
                ('build_time', models.PositiveIntegerField(default=5)),
                ('build_cost', models.PositiveIntegerField(default=200)),
                ('maintenance_cost', models.PositiveIntegerField(default=20)),
                ('water_required', models.PositiveIntegerField(default=15)),
                ('pollution_rate', models.FloatField(default=1.3)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
                ('city_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SewageWorks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('water_required', models.PositiveIntegerField(default=0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('max_employees', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='Oczyszczalnia ścieków', max_length=30)),
                ('build_time', models.PositiveIntegerField(default=2)),
                ('build_cost', models.PositiveIntegerField(default=75)),
                ('maintenance_cost', models.PositiveIntegerField(default=10)),
                ('energy_required', models.PositiveIntegerField(default=5)),
                ('pollution_rate', models.FloatField(default=2.0)),
                ('raw_water', models.PositiveIntegerField(default=0)),
                ('raw_water_required', models.PositiveIntegerField(default=0)),
                ('clean_water_allocated', models.PositiveIntegerField(default=0)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
                ('city_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField(default=0)),
                ('time', models.PositiveIntegerField(default=0)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='WaterTower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('water_required', models.PositiveIntegerField(default=0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('max_employees', models.PositiveIntegerField(default=0)),
                ('raw_water_allocated', models.PositiveIntegerField(default=0)),
                ('raw_water_production', models.PositiveIntegerField(default=0)),
                ('if_waterworks', models.BooleanField(default=True)),
                ('pollution_rate', models.FloatField(default=0.5)),
                ('name', models.CharField(default='Wieża ciśnień', max_length=20)),
                ('build_time', models.PositiveIntegerField(default=1)),
                ('build_cost', models.PositiveIntegerField(default=50)),
                ('maintenance_cost', models.PositiveIntegerField(default=5)),
                ('energy_required', models.PositiveIntegerField(default=3)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
                ('city_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WindPlant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_under_construction', models.BooleanField(default=True)),
                ('current_build_time', models.PositiveIntegerField(default=1)),
                ('energy', models.PositiveIntegerField(default=0)),
                ('energy_required', models.PositiveIntegerField(default=0)),
                ('water', models.PositiveIntegerField(default=0)),
                ('water_required', models.PositiveIntegerField(default=0)),
                ('pollution_product', models.PositiveIntegerField(default=0)),
                ('recycling', models.PositiveIntegerField(default=0)),
                ('max_employees', models.PositiveIntegerField(default=0)),
                ('power_nodes', models.PositiveIntegerField(default=0)),
                ('max_power_nodes', models.PositiveIntegerField(default=1)),
                ('energy_production', models.PositiveIntegerField(default=0)),
                ('energy_allocated', models.PositiveIntegerField(default=0)),
                ('if_electricity', models.BooleanField(default=True)),
                ('name', models.CharField(default='Elektrownia wiatrowa', max_length=20)),
                ('build_time', models.PositiveIntegerField(default=3)),
                ('build_cost', models.PositiveIntegerField(default=100)),
                ('maintenance_cost', models.PositiveIntegerField(default=10)),
                ('pollution_rate', models.FloatField(default=1.8)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City')),
                ('city_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='beanfarm',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.City'),
        ),
        migrations.AddField(
            model_name='beanfarm',
            name='city_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_engine.CityField'),
        ),
    ]
