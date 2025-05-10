from django.urls import path
from . import views

app_name = 'condosync'

urlpatterns = [
    ## Home page
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
    path('encomendas/delete/<int:id>/', views.delete_encomendas, name='delete_encomendas'),

    ## Veículos
    path('veiculos/', views.meus_veiculos, name="meus_veiculos"),
    path('veiculos/adicionar_veiculos/', views.adicionar_veiculos, name="adicionar_veiculos"),
    path('veiculos/gerenciar_veiculos/', views.gerenciar_veiculos, name="gerenciar_veiculos"),
    path('veiculos/editar_veiculos/<int:id>/', views.editar_veiculos, name="editar_veiculos"),
    path('veiculos/deletar_veiculos/<int:id>/', views.deletar_veiculos, name="deletar_veiculos"),
    path('veiculos/admin/', views.veiculos_admin, name="veiculos_admin"),

    ## Ocorrências
    path('ocorrencias/', views.ocorrencias, name='ocorrencias'),
    path('ocorrencias/create/', views.create_ocorrencias, name='create_ocorrencia'),
    path('ocorrencias/edit/<int:id>/', views.edit_ocorrencias, name='edit_ocorrencias'),
    path('ocorrencias/status/<int:id>/', views.status_ocorrencias, name='status_ocorrencias'),
    path('ocorrencias/delete/<int:id>/', views.delete_ocorrencias, name='delete_ocorrencias'),

    ## Sugestões de Melhorias
    path('sugestoes/', views.sugestoes, name='sugestoes'),
    path('sugestoes/create/', views.create_sugestoes, name='create_sugestoes'),
    path('sugestoes/edit/<int:id>', views.edit_sugestoes, name='edit_sugestoes'),
    path('sugestoes/delete/<int:id>', views.delete_sugestoes, name='delete_sugestoes'),

    ## Você sabia...?
    path('voce_sabia/', views.voce_sabia, name='voce_sabia'),

    ## Funcionarios
    path('funcionarios/', views.funcionarios, name='funcionarios'),
    path('funcionarios/create_funcionarios/', views.create_funcionarios, name="create_funcionarios"),
    path('funcionarios/edit_funcionarios/<int:id>/', views.edit_funcionarios, name="edit_funcionarios"),
    path('funcionarios/delete_funcionarios/<int:id>/', views.delete_funcionarios, name="delete_funcionarios"),

    ## Visitantes
    path('visitantes/', views.visitantes, name='visitantes'),
    path('visitantes/create_visitantes/', views.create_visitantes, name='create_visitantes'),
    path('visitantes/gerenciar_visitantes/', views.gerenciar_visitantes, name='gerenciar_visitantes'),
    path('visitantes/delete_visitantes/<int:id>', views.delete_visitantes, name='delete_visitantes'),
    path('visitantes/edit_visitantes/<int:id>', views.edit_visitantes, name='edit_visitantes'),

    ## Reserva de Áreas Comuns
    path('reservas/', views.reservas, name='reservas'),
    path('reservas/criar_reserva/<int:id>', views.criar_reserva, name='criar_reserva'),
    path('reservas/horarios_ocupados/', views.horarios_ocupados, name='horarios_ocupados'),
    path('reservas/listar/<int:id>/', views.listar_reservas_area, name='listar_reservas_area'),
    path('reservas/deletar/<int:id>/', views.delete_reserva, name='delete_reserva'),

]
