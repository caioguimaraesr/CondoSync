from django.urls import path
from . import views

app_name = 'condosync'

urlpatterns = [
    path('home/', views.home, name='home'),
    
    #Boletos
    path('boletos/', views.boletos, name='boletos'),

    ## Avisos
    path('avisos/', views.avisos, name='avisos'),
    path('avisos/create', views.create_avisos, name='create_avisos'),
    path('avisos/edit/<int:id>', views.edit_avisos, name='edit_avisos'),
    path('avisos/delete/<int:id>', views.delete_avisos, name='delete_avisos'),

    ## Encomendas
    path('encomendas/', views.encomendas, name='encomendas'),
    path('encomendas/create', views.create_encomendas, name='create_encomendas'),
    path('encomendas/editar/<int:id>/', views.edit_encomendas, name='edit_encomendas'),
    path('encomendas/delete/<int:id>', views.delete_encomendas, name='delete_encomendas')
]
