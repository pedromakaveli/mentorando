from django.shortcuts import render
from django.http import HttpResponse
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
        
        if senha != confirmar_senha:
            return render(request, "cadastro.html", context={"msg": "As senhas não conferem"})
        else:
            return render(request, "cadastro.html")

def login (request):
    return HttpResponse("Página de Login")