from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Boleto, Apartamento
from django.contrib import messages
# Create your views here.

@login_required(login_url='userauth:login_register')
def home(request):
    return render(request, 'condosync/pages/home.html')

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
