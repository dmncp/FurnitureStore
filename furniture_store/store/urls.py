from django.urls import path
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    # path('contact', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('contact', contactView, name='contact'),
    path('contact/success/', successView, name='success'),
]
