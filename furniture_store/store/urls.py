from django.urls import path
from django.views.generic.base import TemplateView
from .views import SignUpView


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
]
