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
    path('settings/address/edit/<int:pk>', AddressEditFormView.as_view(template_name='address_edit_form.html'), name='address_form')
]
