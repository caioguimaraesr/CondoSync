from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Boleto, Apartamento, Aviso, Encomenda
from django.contrib import messages
from django.utils import timezone
# Create your views here.
def is_admin(user):
    if not user.is_superuser:
        return False 
    return True

########################### Home Page ###################################
@login_required(login_url='userauth:login_register')
def home(request):
    return render(request, 'condosync/pages/home.html')

########################### Boletos ###################################
@login_required(login_url='userauth:login_register')
def boletos(request):
    apartamento = get_object_or_404(Apartamento, morador=request.user)
    boletos = Boleto.objects.filter(apartamentos=apartamento)

    if request.user.is_superuser:
        apartamentos = Apartamento.objects.all()
    else:
        apartamentos = None 

    if request.method == 'POST':
        apartamento_id = request.POST.get('apartamento')
        mes_referencia = request.POST.get('mes_referencia')
        arquivo = request.FILES.get('arquivo')

        apartamento = get_object_or_404(Apartamento, id=apartamento_id)

        if arquivo:
            boleto = Boleto(
                apartamentos=apartamento,
                mes_referencia=mes_referencia,
                arquivo=arquivo
            )
            boleto.save()
            messages.success(request, 'Boleto cadastrado com sucesso.')
            return redirect('condosync:boletos')

    return render(request, 'condosync/pages/boletos.html', {
        'boletos': boletos,
        'apartamentos': apartamentos 
    })

############################### Avisos ##############################################
@login_required(login_url='userauth:login_register')
def avisos(request):
    avisos = Aviso.objects.order_by('-data_postagem')
    return render(request, "condosync/pages/avisos/avisos.html", context={
        'avisos':avisos
    })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:avisos')
def create_avisos(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        if titulo and conteudo:
            Aviso.objects.create(titulo=titulo, conteudo=conteudo, data_postagem=timezone.now())
            return redirect('condosync:avisos')
    return render(request, 'condosync/pages/avisos/create_avisos.html', context={
        'acao': 'Adicionar'
        })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:avisos')
def edit_avisos(request, id):
    aviso = get_object_or_404(Aviso, id=id)
    if request.method == 'POST':
        aviso.titulo = request.POST.get('titulo')
        aviso.conteudo = request.POST.get('conteudo')
        aviso.save()
        return redirect('condosync:avisos')
    return render(request, 'condosync/pages/avisos/edit_avisos.html', context={
        'aviso': aviso, 
        'acao': 'Editar'
        })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:avisos')
def delete_avisos(request, id):
    aviso = get_object_or_404(Aviso, id=id)
    if request.method == 'POST':
        aviso.delete()
        messages.success(request, 'Aviso excluído com sucesso!!')
        return redirect('condosync:avisos')
    return render(request, 'condosync/pages/avisos/delete_avisos.html', context={
        'aviso': aviso
        })

############################### Encomendas ##############################################
@login_required(login_url='condosync:login_register')
def encomendas(request):
    encomendas = Encomenda.objects.select_related('apartamento__morador').order_by('-data_chegada')
    return render(request, 'condosync/pages/encomendas/encomendas.html', {
        'encomendas': encomendas
    })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:avisos')
def create_encomendas(request):
    apartamentos = Apartamento.objects.all()

    if request.method == 'POST':
        apartamento_id = request.POST.get('apartamento')
        peso_kg = request.POST.get('peso_kg')
        origem = request.POST.get('origem')

        if apartamento_id and peso_kg and origem:
            Encomenda.objects.create(
                apartamento=Apartamento.objects.get(id=apartamento_id),
                peso_kg=peso_kg,
                origem=origem,
                data_chegada=timezone.now(),
            )
            return redirect('condosync:encomendas')

    return render(request, 'condosync/pages/encomendas/create_encomendas.html', context={
        'apartamentos': apartamentos
        })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:avisos')
def edit_encomendas(request, id):
    encomenda = get_object_or_404(Encomenda, id=id)
    apartamentos = Apartamento.objects.all()

    if request.method == 'POST':
        apartamento_id = request.POST.get('apartamento')
        peso_kg = request.POST.get('peso_kg')
        origem = request.POST.get('origem')

        if apartamento_id and peso_kg and origem:
            encomenda.apartamento = get_object_or_404(Apartamento, id=apartamento_id)
            encomenda.peso_kg = peso_kg
            encomenda.origem = origem
            encomenda.save()
            return redirect('condosync:encomendas')

    return render(request, 'condosync/pages/encomendas/edit_encomendas.html', {
        'encomenda': encomenda,
        'apartamentos': apartamentos,
        'editando': True
    })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:avisos')
def delete_encomendas(request, id):
    encomenda = get_object_or_404(Encomenda, id=id)
    if request.method == 'POST':
        encomenda.delete()
        return redirect('condosync:encomendas')
    return render(request, 'condosync/pages/encomendas/delete_encomendas.html', context={
        'encomenda':encomenda
    })