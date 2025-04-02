from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.

def cadastro (request):
    
    if request.method == "GET":
        return render(request, "cadastro.html")
    elif request.method == "POST":
        dados = {
            'username': request.POST.get('username'),
            'senha': request.POST.get('senha'),
            'confirmar_senha': request.POST.get('confirmar_senha')
        }
        
        
        username = dados["username"]
        senha = dados["senha"]
        confirmar_senha = dados["confirmar_senha"]
        users = User.objects.filter(username=username)
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, "Senha e confirmar senha devem ser iguais.")
            return redirect("cadastro")
        
        elif len(senha) < 6:
            messages.add_message(request, constants.ERROR, "A senha deve ter 6 ou mais caracteres.")
            return redirect("cadastro")
        
        elif users.exists():
            messages.add_message(request, constants.ERROR, "Já existe um usuário com esse username.")
            return redirect("cadastro")
        
        else:
            User.objects.create_user(
                username=username,
                password=senha
            )
            
            return redirect("login")

def login (request):
    
    if request.method == "GET":
        return render(request, "login.html")