# Generated by Django 5.0.3 on 2024-04-13 17:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0002_maintenance_status_at_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuelType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fueltype', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='vehicle',
            name='fueltype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehicles.fueltype'),
        ),
    ]