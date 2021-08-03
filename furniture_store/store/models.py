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
class Address(models.Model):
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_nr = models.CharField(max_length=5)
    building_nr = models.CharField(max_length=5, blank=True)
    zip_code = models.CharField(max_length=7)

    def __str__(self):
        return str(self.city) + ',' + str(self.street) + ' ' + str(self.building_nr) + '/' + str(self.house_nr)


class FurnitureType(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(default='', blank=True)

    def __str__(self):
        return str(self.name)


class Furniture(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(FurnitureType, on_delete=models.CASCADE)
    state = models.CharField(choices=STATE, default='new', max_length=20)
    price = models.FloatField(default=200)
    origin = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    description = models.TextField()
    warranty_time = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    height = models.IntegerField()
    width = models.IntegerField()
    depth = models.IntegerField()
    url1 = models.URLField(default='', blank=True)
    url2 = models.URLField(default='', blank=True)
    url3 = models.URLField(default='', blank=True)

    @property
    def price_with_discount(self):
        return round(self.price * (1 - self.discount / 100), 2)

    def __str__(self):
        return str(self.name)


class Opinion(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    rating = models.IntegerField()
    opinion = models.TextField()

    def __str__(self):
        return str(self.opinion)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, default=0)


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.user)


class OrderProduct(models.Model):
    product = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return str(self.product.name) + ':' + str(self.amount)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    order_nr = models.CharField(max_length=7)
    price = models.FloatField()
    products = models.ManyToManyField(OrderProduct, symmetrical=False, related_name='ordered_products')
    status = models.CharField(choices=ORDER_STATUS, default='unsent', max_length=20)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return str(self.user) + ':' + str(self.order_nr)


