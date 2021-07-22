from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(FurnitureType)
class FurnitureTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'price', 'discount', 'amount', 'state']
    list_filter = ['name', 'type', 'price', 'state']


@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ['id', 'furniture', 'user', 'rating']
    list_filter = ['furniture', 'user', 'rating']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'furniture']
    list_filter = ['user', 'furniture']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'city', 'street', 'house_nr', 'building_nr', 'zip_code']
    list_filter = ['city', 'street', 'house_nr', 'zip_code', 'building_nr']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_nr', 'price', 'status']
    list_filter = ['user', 'price', 'order_nr', 'status']


@admin.register(UserAddress)
class UserAddress(admin.ModelAdmin):
    list_display = ['id', 'user', 'address']
    list_filter = ['user', 'address']


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'amount']
    list_filter = ['product', 'amount']

