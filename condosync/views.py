from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Boleto, Apartamento, Aviso, Encomenda, Veiculo, Ocorrencia, Sugestoes, VoceSabia, Funcionario, Visitante, AreaComum, Horario, Reserva
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import ValidationError

# Create your views here.
def is_admin(user):
    if not user.is_superuser:
        return False 
    return True

def is_user(user):
    if not user.is_authenticated or user.is_superuser:
        return False
    return True

########################### Home Page ###################################
@login_required(login_url='userauth:login_register')
def home(request):
    informacao = VoceSabia.objects.last()
    return render(request, 'condosync/pages/home.html', context={
        'informacao': informacao
    })

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

    return render(request, 'condosync/pages/encomendas/edit_encomendas.html', context={
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

#################################### Carros ##############################################
@login_required(login_url='userauth:login_register')
@user_passes_test(is_user, login_url='condosync:veiculos_admin')
def meus_veiculos(request):
    usuario = request.user
    veiculos = Veiculo.objects.filter(usuario=usuario)
    return render(request, 'condosync/pages/veiculos/meus_veiculos.html', context={
        'veiculos':veiculos
    })

@login_required(login_url='userauth:login_register')
def adicionar_veiculos(request):
    veiculos_do_usuario = Veiculo.objects.filter(usuario=request.user)
    if veiculos_do_usuario.count() >= 5:
        messages.error(request, 'Você já atingiu o limite de 5 veículos cadastrados.')
        return redirect('condosync:meus_veiculos')

    if request.method == 'POST':
        tipo_veiculo = request.POST.get('tipo_veiculo')
        modelo = request.POST.get('modelo')
        placa = request.POST.get('placa')
        cor = request.POST.get('cor')
        ano = request.POST.get('ano')
        marca = request.POST.get('marca')

        veiculo = Veiculo(
            tipo_veiculo=tipo_veiculo,
            modelo=modelo,
            placa=placa,
            cor=cor,
            ano=ano,
            marca=marca,
            usuario=request.user
        )
        veiculo.save()
        return redirect('condosync:meus_veiculos')
    return render(request, 'condosync/pages/veiculos/adicionar_veiculos.html')

@login_required(login_url='userauth:login_register')
def gerenciar_veiculos(request):
    usuario = request.user
    veiculos = Veiculo.objects.filter(usuario=usuario)
    return render(request, 'condosync/pages/veiculos/gerenciar_veiculos.html', context={
        'veiculos': veiculos
    })

@login_required(login_url='userauth:login_register')
def editar_veiculos(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)

    if request.method == 'POST':
        tipo_veiculo = request.POST.get('tipo_veiculo')
        modelo = request.POST.get('modelo')
        placa = request.POST.get('placa')
        cor = request.POST.get('cor')
        marca = request.POST.get('marca')
        ano = request.POST.get('ano')

        if tipo_veiculo and placa and marca and modelo and cor and ano:
            veiculo.tipo_veiculo = tipo_veiculo
            veiculo.placa = placa
            veiculo.marca = marca
            veiculo.modelo = modelo
            veiculo.cor = cor
            veiculo.ano = ano
            veiculo.save()
            return redirect('condosync:meus_veiculos') 

    return render(request, 'condosync/pages/veiculos/editar_veiculos.html', context={
        'veiculo': veiculo 
    })

@login_required(login_url='userauth:login_register')
def deletar_veiculos(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if request.method == 'POST':
        veiculo.delete()
        if not is_admin:
            return redirect('condosync:meus_veiculos')
        else:
            return redirect('condosync:veiculos_admin')
    return render(request, 'condosync/pages/veiculos/deletar_veiculos.html', context={
        'veiculo': veiculo
    })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:meus_veiculos')
def veiculos_admin(request):
    if request.user.is_superuser:
        search_query = request.GET.get('search', '')

        veiculos = Veiculo.objects.filter(
            tipo_veiculo__icontains=search_query
        ) | Veiculo.objects.filter(
            modelo__icontains=search_query
        ) | Veiculo.objects.filter(
            placa__icontains=search_query
        ) | Veiculo.objects.filter(
            marca__icontains=search_query
        )
        
        return render(request, 'condosync/pages/veiculos/veiculos_admin.html', context={
            'veiculos': veiculos,
            'search_query': search_query
        })
    else:
        return redirect('condosync:veiculos')
    
#################################### Ocorrências ##############################################
@login_required(login_url='userauth:login_register')
def ocorrencias(request):
    ocorrencias = Ocorrencia.objects.all().order_by('-created_at')
    return render(request, 'condosync/pages/ocorrencias/ocorrencias.html', context={
        'ocorrencias': ocorrencias
    })

@login_required(login_url='userauth:login_register')
def create_ocorrencias(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        desc = request.POST.get('desc')
        status = request.POST.get('status', 'pendente')

        Ocorrencia.objects.create(
            titulo=titulo,
            desc=desc,
            status=status,
            usuario=request.user
        )
        return redirect('condosync:ocorrencias')
    
    return render(request, 'condosync/pages/ocorrencias/create_ocorrencias.html')

@login_required(login_url='userauth:login_register')
def edit_ocorrencias(request, id):
    ocorrencia = get_object_or_404(Ocorrencia, id=id)

    if request.user != ocorrencia.usuario and not request.user.is_superuser:
        return redirect('condosync:ocorrencias') 

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        desc = request.POST.get('desc')

        if titulo and desc:
            ocorrencia.titulo = titulo
            ocorrencia.desc = desc
            ocorrencia.save()
            return redirect('condosync:ocorrencias')

    return render(request, 'condosync/pages/ocorrencias/edit_ocorrencias.html', context={
        'ocorrencia': ocorrencia
    })

@login_required(login_url='userauth:login_register')
def delete_ocorrencias(request, id):
    ocorrencia = get_object_or_404(Ocorrencia, id=id)

    if request.user != ocorrencia.usuario and not request.user.is_superuser:
        return redirect('condosync:ocorrencias') 

    if request.method == 'POST':
        ocorrencia.delete()
        return redirect('condosync:ocorrencias')

    return render(request, 'condosync/pages/ocorrencias/delete_ocorrencias.html', context={
        'ocorrencia': ocorrencia
    })

@login_required(login_url='userauth:login_register')
def status_ocorrencias(request, id):
    ocorrencia = get_object_or_404(Ocorrencia, id=id)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pendente', 'em_andamento', 'resolvido']:
            ocorrencia.status = status
            ocorrencia.save()
            return redirect('condosync:ocorrencias')
    
    return render(request, 'condosync/pages/ocorrencias/status_ocorrencias.html', {
        'ocorrencia': ocorrencia
    })

#################################### Sugestões Melhorias ##############################################
def sugestoes(request):
    sugestoes = Sugestoes.objects.all().order_by('-data_criacao')
    return render(request, 'condosync/pages/sugestoes_melhorias/sugestoes_melhorias.html', context={
        'sugestoes':sugestoes
    })

def create_sugestoes(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        if titulo and descricao:
            Sugestoes.objects.create(
                usuario=request.user,
                titulo=titulo,
                descricao=descricao
            )
            return redirect('condosync:sugestoes') 
    return render(request, 'condosync/pages/sugestoes_melhorias/create_sugestoes.html')

def edit_sugestoes(request, id):
    sugestao = get_object_or_404(Sugestoes, id=id)

    if sugestao.usuario != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Você não tem permissão para editar esta sugestão.")

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        if titulo and descricao:
            sugestao.titulo = titulo
            sugestao.descricao = descricao
            sugestao.save()
            return redirect('condosync:sugestoes')

    return render(request, 'condosync/pages/sugestoes_melhorias/edit_sugestoes.html', context={
        'sugestao': sugestao
    })


def delete_sugestoes(request, id):
    sugestao = get_object_or_404(Sugestoes, id=id)

    if sugestao.usuario != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Você não tem permissão para excluir esta sugestão.")

    if request.method == 'POST':
        sugestao.delete()
        return redirect('condosync:sugestoes')

    return render(request, 'condosync/pages/sugestoes_melhorias/delete_sugestoes.html', context={
        'sugestao': sugestao
    })

#################################### Você sabia? ##############################################
def voce_sabia(request):
    informacao = VoceSabia.objects.last()

    if not informacao:
        informacao = VoceSabia.objects.create(
            titulo_1='', conteudo_1='',
            titulo_2='', conteudo_2=''
        )

    if request.method == 'POST':
        informacao.titulo_1 = request.POST.get('titulo_1', '')
        informacao.conteudo_1 = request.POST.get('conteudo_1', '')
        informacao.titulo_2 = request.POST.get('titulo_2', '')
        informacao.conteudo_2 = request.POST.get('conteudo_2', '')
        informacao.save()
        return redirect('condosync:home')

    return render(request, 'condosync/pages/voce_sabia.html', {
        'informacao': informacao
    })

#################################### Funcionarios ##############################################
@login_required(login_url='userauth:login_register')
def funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'condosync/pages/funcionarios/funcionarios.html', context={
        'funcionarios': funcionarios
        })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:funcionarios')
def create_funcionarios(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cargo = request.POST.get('cargo')

        Funcionario.objects.create(
            nome=nome,
            cargo=cargo,
        )

        return redirect('condosync:funcionarios')  

    return render(request, 'condosync/pages/funcionarios/create_funcionarios.html')

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:funcionarios')
def edit_funcionarios(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        cargo = request.POST.get('cargo')

        funcionario.nome = nome
        funcionario.cargo = cargo
        funcionario.save()

        return redirect('condosync:funcionarios')

    return render(request, 'condosync/pages/funcionarios/edit_funcionarios.html', context={
        'funcionario': funcionario
        })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:funcionarios')
def delete_funcionarios(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        funcionario.delete()
        return redirect('condosync:funcionarios')

    return render(request, 'condosync/pages/funcionarios/delete_funcionarios.html', context={
        'funcionario': funcionario
        })

#################################### Funcionarios ##############################################
@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:home')
def visitantes(request):
    visitantes = Visitante.objects.all().order_by('-data_visita')
    return render(request, 'condosync/pages/visitantes/visitantes.html', {
        'visitantes': visitantes
    })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:home')
def create_visitantes(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        apartamento_id = request.POST.get('apartamento')

        if Visitante.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já cadastrado!')
            return redirect('condosync:create_visitantes')
        
        if nome and cpf and apartamento_id:
            apartamento = Apartamento.objects.get(id=apartamento_id)
            visitante = Visitante(
                nome=nome,
                cpf=cpf,
                apartamento=apartamento
            )
            visitante.save()
            return redirect('condosync:visitantes') 

    apartamentos = Apartamento.objects.all()
    return render(request, 'condosync/pages/visitantes/create_visitantes.html', context={
        'apartamentos': apartamentos
        })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:home')
def gerenciar_visitantes(request):
    visitantes = Visitante.objects.all()
    return render(request, 'condosync/pages/visitantes/gerenciar_visitantes.html', context={
        'visitantes': visitantes
    })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:home')
def delete_visitantes(request, id):
    visitante = get_object_or_404(Visitante, id=id)

    if request.method == 'POST':
        visitante.delete()
        return redirect('condosync:gerenciar_visitantes')

    return render(request, 'condosync/pages/visitantes/delete_visitantes.html', context={
        'visitante': visitante
    })

@login_required(login_url='userauth:login_register')
@user_passes_test(is_admin, login_url='condosync:home')
def edit_visitantes(request, id):
    visitante = get_object_or_404(Visitante, id=id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        apartamento_id = request.POST.get('apartamento')

        visitante.nome = nome
        visitante.cpf = cpf
        visitante.apartamento = get_object_or_404(Apartamento, id=apartamento_id)
        visitante.save()

        return redirect('condosync:gerenciar_visitantes')

    apartamentos = Apartamento.objects.all()

    return render(request, 'condosync/pages/visitantes/edit_visitantes.html', context={
        'visitante': visitante,
        'apartamentos': apartamentos
    })

#################################### Reservas ##############################################
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import AreaComum, Horario, Reserva

def reservas(request):
    areas = AreaComum.objects.all()
    return render(request, 'condosync/pages/reservas/reservas.html', {'areas': areas})

def criar_reserva(request, id):
    area = get_object_or_404(AreaComum, id=id)
    horarios = Horario.objects.all()

    if request.method == 'POST':
        data = request.POST.get('data')
        horario_id = request.POST.get('horario')
        horario = get_object_or_404(Horario, id=horario_id)

        if Reserva.objects.filter(area=area, data=data, horario=horario).exists():
            messages.error(request, 'Já existe uma reserva para essa área nesse horário.')
            return redirect('condosync:criar_reserva', id=area.id)

        Reserva.objects.create(
            usuario=request.user,
            area=area,
            data=data,
            horario=horario
        )
        messages.success(request, 'Reserva realizada com sucesso!')
        return redirect('condosync:reservas')

    return render(request, 'condosync/pages/reservas/criar_reserva.html', {
        'area': area,
        'horarios': horarios
    })

def horarios_ocupados(request):
    area_id = request.GET.get('area_id')
    data = request.GET.get('data')

    reservas = Reserva.objects.filter(area_id=area_id, data=data)
    horarios_ocupados = reservas.values_list('horario_id', flat=True)

    return JsonResponse(list(horarios_ocupados), safe=False)

@login_required
def listar_reservas_area(request, id):
    area = get_object_or_404(AreaComum, id=id)
    reservas = Reserva.objects.filter(area=area).order_by('data', 'horario')

    return render(request, 'condosync/pages/reservas/listar_reservas.html', {
        'area': area,
        'reservas': reservas
    })

@login_required
def delete_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    if request.user == reserva.usuario or request.user.is_superuser:
        reserva.delete()
        messages.success(request, "Reserva deletada com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para deletar essa reserva.")

    return redirect('condosync:listar_reservas_area', id=reserva.area.id)

################################### Área Comum ########################################

def adicionar_area(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        icone = request.POST.get("icone")
        ativo = request.POST.get("ativo") == "on"

        AreaComum.objects.create(
            nome=nome,
            icone=icone,
            ativo=ativo
        )

        return redirect('condosync:reservas')

    return render(request, 'condosync/pages/reservas/adicionar_area.html')

def gerenciar_area(request):
    areas = AreaComum.objects.all()
    return render(request, 'condosync/pages/reservas/gerenciar_area.html', context={
        'areas': areas
    })

def delete_area(request, id):
    area = get_object_or_404(AreaComum, id=id)

    if request.user.is_superuser:
        area.delete()
        messages.success(request, "Área comum deletada com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para deletar esta área.")

    return redirect('condosync:gerenciar_area')

