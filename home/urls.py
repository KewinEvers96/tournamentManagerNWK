from django.urls import path
from django.views.generic.base import TemplateView
from .views import RegistrationView

app_name = 'home'
urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='index'),
    path('signUp', RegistrationView.as_view(), name='signUp'),
]
