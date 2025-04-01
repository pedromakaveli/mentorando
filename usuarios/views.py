from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
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
            return render(request, "cadastro.html", context={"msg": "As senhas não conferem"})
        
        elif len(senha) < 6:
            return redirect("cadastro")
        
        elif users.exists():
            return redirect("cadastro")
        
        else:
            User.objects.create_user(
                username=username,
                password=senha
            )
            
            return redirect ("/usuarios/login")

def login (request):
    return HttpResponse("Página de Login")