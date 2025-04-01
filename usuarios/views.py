from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def cadastro (request):
    
    if request.method == "GET":
        return render(request, "cadastro.html")
    elif request.method == "POST":
        dados = request.body()
        print(dados)
        return dados

def login (request):
    return HttpResponse("Página de Login")