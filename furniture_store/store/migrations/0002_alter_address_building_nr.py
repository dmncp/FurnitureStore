# Generated by Django 3.2 on 2021-07-21 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='building_nr',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
