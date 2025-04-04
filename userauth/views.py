from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from condosync.models import Apartamento

def login_register_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'register':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            apartamento_id = request.POST.get('apartamento')

            admin = request.POST.get('admin')  
            usuario = request.POST.get('usuario')  
            admin_password = request.POST.get('admin_password')

            if password != confirm_password:
                messages.error(request, "As senhas não coincidem.")
                return redirect('userauth:login_register')

            if User.objects.filter(username=username).exists():
                messages.error(request, "O nome de usuário já está em uso.")
                return redirect('userauth:login_register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Este e-mail já está registrado.")
                return redirect('userauth:login_register')

            if admin:
                if admin_password != 'senha':
                    messages.error(request, 'Senha de administrador incorreta.')
                    return redirect('userauth:login_register')

                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                messages.success(request, 'Usuário administrador cadastrado com sucesso.')
                return redirect('userauth:login_register')

            elif usuario:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()

                if apartamento_id:
                    apartamento = Apartamento.objects.get(id=apartamento_id)
                    apartamento.morador = user
                    apartamento.save()

                messages.success(request, "Cadastro realizado com sucesso! Faça login.")
                return redirect('userauth:login_register')

        elif form_type == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password') 

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('condosync:home')
            else:
                messages.error(request, "Credenciais inválidas. Tente novamente.")
                return redirect('userauth:login_register')

    apartamentos_disponiveis = Apartamento.objects.filter(morador__isnull=True)
    
    return render(request, 'userauth/pages/login_register.html', context={
        'apartamentos':apartamentos_disponiveis
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('userauth:login_register')
