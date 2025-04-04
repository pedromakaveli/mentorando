from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Mentorados
from .models import Navigators
from django.contrib import messages

# Create your views here.

def mentorados (request):
    if request.method == "GET":
        navigators = Navigators.objects.filter(user=request.user)
        return render(request, 'mentorados.html', {'estagios': Mentorados.estagio_choices, 'navigators': navigators})
    elif request.method == "POST":
        nome = request.POST.get("nome")
        estagio = request.POST.get("estagio")
        navigator = request.POST.get("navigator")
        foto = request.POST.get("foto")
        
        mentorado = Mentorados.objects.filter(nome=nome)
        if mentorado.exists():
            print("O mentorado já existe")
            messages.add_message(request, messages.ERROR, "Esse mentorado já existe.")
            return redirect ("mentorados")

        mentorado = Mentorados(
            nome=nome,
            estagio=estagio,
            navigator_id=navigator,
            foto=foto,
            user=request.user
        )
        
        
        mentorado.save()
        messages.add_message(request, messages.SUCCESS, f"O mentorado {nome} foi cadastrado com sucesso")
        return redirect ("mentorados")