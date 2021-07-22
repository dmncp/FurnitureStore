from django.urls import path
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('contact', contactView, name='contact'),
    path('settings', settings_view, name='settings'),
    path('settings/profile', EditProfileView.as_view(), name='profile'),
    path('settings/address', AddressEditView.as_view(template_name='address_edit.html'), name='address'),
    path('settings/address/edit/<int:pk>', AddressEditFormView.as_view(template_name='address_edit_form.html'), name='address_form'),
    path('settings/address/delete/<int:pk>', delete_address, name='address_delete'),
    path('settings/customer_orders', CustomerOrdersView.as_view(template_name='customer_orders.html'), name='customer_orders'),
    path('settings/customer_orders/details/<int:pk>', OrderDetailsView.as_view(template_name='order_details.html'), name='order_details'),
    path('settings/opinions', OpinionsView.as_view(template_name='opinions.html'), name='opinions'),
    path('settings/opinions/delete/<int:pk>', delete_opinion, name='delete_opinion'),
    path('settings/opinions/edit/<int:pk>', OpinionEditFormView.as_view(template_name='opinions_edit.html'), name='opinion_edit'),
    path('settings/delete_account', delete_account, name='delete_user'),
    path('settings/delete_confirm', TemplateView.as_view(template_name='delete_user.html'), name='delete_user_confirmation')
]
