# Generated by Django 3.2 on 2021-07-29 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='address',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='store.useraddress'),
        ),
    ]
