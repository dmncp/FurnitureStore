# Generated by Django 3.2 on 2021-08-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_furniture_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='opinion',
            field=models.TextField(blank=True),
        ),
    ]
