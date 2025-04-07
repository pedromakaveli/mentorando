from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Mentorados
from .models import Navigators
from .models import Disponibilidade as DisponibilidadeHorarios
from .models import Reuniao
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from mentorados.auth import valida_token
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
        reunioes = Reuniao.objects.filter(data__mentor=request.user)
        return render(request, "reunioes.html", {'reunioes': reunioes})
    
    elif request.method == "POST":
        data = request.POST.get("data")
        data = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        disponibilidades = DisponibilidadeHorarios.objects.filter(
                    data_inicial__gte=(data - timedelta(minutes=50)),
                    data_inicial__lte=(data + timedelta(minutes=50))
                )

        if disponibilidades.exists():
            messages.add_message(request, messages.ERROR, 'Você já possui uma reunião em aberto.')
            return redirect('reunioes')

        disponibilidade = DisponibilidadeHorarios(
            data_inicial=data,
            mentor=request.user

        )
        disponibilidade.save()

        messages.add_message(request, messages.SUCCESS, 'Horário disponibilizado com sucesso.')
        return redirect('reunioes')

def auth(request):
    if request.method == 'GET':
        return render(request, 'auth_mentorado.html')
    
    else:
        token = request.POST.get('token')

        if not Mentorados.objects.filter(token=token).exists():
            messages.add_message(request, messages.ERROR, 'Token inválido')
            return redirect('auth_mentorado')
        
        response = redirect('escolher_dia')
        response.set_cookie('auth_token', token, max_age=3600)
        return response
    
def escolher_dia(request):
    if not valida_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentorado')
    if request.method == 'GET':
        disponibilidades = DisponibilidadeHorarios.objects.filter(
            data_inicial__gte=datetime.now(),
            agendado=False
        ).values_list('data_inicial', flat=True)
        horarios = []
        for i in disponibilidades:
            horarios.append(i.date().strftime('%d-%m-%Y'))


        return render(request, 'escolher_dia.html', {'horarios': list(set(horarios))})

def agendar_reuniao(request):
    
    if not valida_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentorado')
    
    if request.method == 'GET':
        data = request.GET.get("data")
        data = datetime.strptime(data, '%d-%m-%Y')
        horarios = DisponibilidadeHorarios.objects.filter(
            data_inicial__gte=data,
            data_inicial__lt=data + timedelta(days=1),
            agendado=False
        )
        return render(request, 'agendar_reuniao.html', {'horarios': horarios, 'tags': Reuniao.tag_choices})
    
    else:
        horario_id = request.POST.get('horario')
        tag = request.POST.get('tag')
        descricao = request.POST.get("descricao")

        reuniao = Reuniao(
            data_id=horario_id,
            mentorado=valida_token(request.COOKIES.get('auth_token')),
            tag=tag,
            descricao=descricao
        )
        reuniao.save()

        horario = DisponibilidadeHorarios.objects.get(id=horario_id)
        horario.agendado = True
        horario.save()

        messages.add_message(request, messages.SUCCESS, 'Reunião agendada com sucesso.')
        return redirect('escolher_dia')