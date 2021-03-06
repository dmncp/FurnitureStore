# Generated by Django 3.2 on 2021-07-13 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('house_nr', models.CharField(max_length=5)),
                ('building_nr', models.CharField(max_length=5)),
                ('zip_code', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('state', models.CharField(choices=[('new', 'Nowy'), ('used', 'Używany')], default='new', max_length=20)),
                ('price', models.IntegerField(default=200)),
                ('origin', models.CharField(max_length=255)),
                ('material', models.CharField(max_length=255)),
                ('amount', models.IntegerField(default=0)),
                ('description', models.TextField()),
                ('warranty_time', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=0)),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('depth', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FurnitureType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='store.address')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('furniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.furniture')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_nr', models.CharField(max_length=7)),
                ('price', models.IntegerField()),
                ('status', models.CharField(choices=[('unsent', 'Zamówienie nie zostało jeszcze wysłane'), ('sent', 'Zamówienie zostało wysłane. Jest już w drodze'), ('ordered', 'Zamówienie zostało dostarczone')], default='unsent', max_length=20)),
                ('products', models.ManyToManyField(related_name='ordered_products', to='store.Furniture')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('opinion', models.TextField()),
                ('furniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.furniture')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='furniture',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.furnituretype'),
        ),
    ]
