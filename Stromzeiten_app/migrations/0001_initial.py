# Generated by Django 3.1.3 on 2020-11-04 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Generation',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('Biomass', models.IntegerField()),
                ('Fossil_Brown_coal_Lignite', models.IntegerField()),
                ('Fossil_Gas', models.IntegerField()),
                ('Fossil_Hard_coal', models.IntegerField()),
                ('Fossil_Oil', models.IntegerField()),
                ('Geothermal', models.IntegerField()),
                ('Hydro_Pumped_Storage', models.IntegerField()),
                ('Hydro_Run_of_river_and_poundage', models.IntegerField()),
                ('Hydro_Water_Reservoir', models.IntegerField()),
                ('Nuclear', models.IntegerField()),
                ('Other', models.IntegerField()),
                ('Other_renewable', models.IntegerField()),
                ('Solar', models.IntegerField()),
                ('Waste', models.IntegerField()),
                ('Wind_Offshore', models.IntegerField()),
                ('Wind_Onshore', models.IntegerField()),
                ('Date', models.CharField(max_length=100)),
                ('Total_Non_Renewables', models.IntegerField()),
                ('Total_Renewables', models.IntegerField()),
                ('Total', models.IntegerField()),
                ('Renewables_procentaqe', models.IntegerField()),
            ],
        ),
    ]
