# Generated by Django 3.1.5 on 2021-09-17 11:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_project_cargo', '0007_auto_20210916_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='send_cargo',
            name='cargo_distance',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(1e-06), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]
