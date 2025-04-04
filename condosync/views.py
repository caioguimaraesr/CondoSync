from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Boleto, Apartamento, Aviso
from django.contrib import messages
from django.utils import timezone
# Create your views here.
def is_admin(user):
    if not user.is_superuser:
        return False 
    return True

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
        'aviso': aviso, 'acao': 'Editar'
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