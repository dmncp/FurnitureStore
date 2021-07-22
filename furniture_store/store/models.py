from django.db import models
from django.contrib.auth.models import User

STATE = (
    ('new', 'Nowy'),
    ('used', 'Używany')
)

ORDER_STATUS = (
    ('unsent', 'Zamówienie nie zostało jeszcze wysłane'),
    ('sent', 'Zamówienie zostało wysłane. Jest już w drodze'),
    ('ordered', 'Zamówienie zostało dostarczone')
)


# Create your models here.
class FurnitureType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Furniture(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(FurnitureType, on_delete=models.CASCADE)
    state = models.CharField(choices=STATE, default='new', max_length=20)
    price = models.IntegerField(default=200)
    origin = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    description = models.TextField()
    warranty_time = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    height = models.IntegerField()
    width = models.IntegerField()
    depth = models.IntegerField()


class Opinion(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    rating = models.IntegerField()
    opinion = models.TextField()


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)


class Address(models.Model):
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_nr = models.CharField(max_length=5)
    building_nr = models.CharField(max_length=5, blank=True)
    zip_code = models.CharField(max_length=7)


class OrderProduct(models.Model):
    product = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    order_nr = models.CharField(max_length=7)
    price = models.IntegerField()
    products = models.ManyToManyField(OrderProduct, symmetrical=False, related_name='ordered_products')
    status = models.CharField(choices=ORDER_STATUS, default='unsent', max_length=20)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, default=0)

