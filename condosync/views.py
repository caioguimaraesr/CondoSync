from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='userauth:login_register')
def home(request):
    return render(request, 'condosync/pages/home.html')