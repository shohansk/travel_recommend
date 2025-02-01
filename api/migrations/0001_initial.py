# Generated by Django 5.0.11 on 2025-02-01 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DistrictsLocations',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('division_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('bn_name', models.CharField(max_length=255)),
                ('lat', models.DecimalField(decimal_places=8, max_digits=10)),
                ('long', models.DecimalField(decimal_places=8, max_digits=10)),
            ],
            options={
                'db_table': 'districts_locations',
            },
        ),
    ]
