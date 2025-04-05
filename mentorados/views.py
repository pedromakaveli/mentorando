from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Mentorados
from .models import Navigators
from .models import Disponibilidade as DisponibilidadeHorarios
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.

@login_required
def mentorados (request):
    if request.method == "GET":
        navigators = Navigators.objects.filter(user=request.user)
        mentorados = Mentorados.objects.filter(user=request.user)
        
        estagios_flat = [i[1] for i in Mentorados.estagio_choices]
        qtd_estagios = []
        
        for i, j in Mentorados.estagio_choices:
            x = Mentorados.objects.filter(estagio=j, user=request.user).count()
            qtd_estagios.append(x)
        
        return render(request, 'mentorados.html', {'estagios': Mentorados.estagio_choices, 'navigators': navigators, 'mentorados': mentorados, 'estagios_flat': estagios_flat, 'qtd_estagios': qtd_estagios})
    
    elif request.method == "POST":
        nome = request.POST.get("nome")
        estagio = request.POST.get("estagio")
        navigator = request.POST.get("navigator")
        foto = request.FILES.get("foto")
        
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
    

def reunioes (request):
    if request.method == "GET":
        return render(request, "reunioes.html")
    
    elif request.method == "POST":
        data = request.POST.get("data")
        data = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        disponibilidades = DisponibilidadeHorarios(
            data_inicial = data,
            mentor=request.user
        ).save()
        
        return HttpResponse(data)