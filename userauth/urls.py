from django.urls import path, include
from . import views

app_name = 'userauth'

urlpatterns = [
    path('', views.login_register_view, name='login_register')
]
