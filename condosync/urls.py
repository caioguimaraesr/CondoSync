from django.urls import path
from . import views

app_name = 'condosync'

urlpatterns = [
    path('home/', views.home, name='home'),
]
