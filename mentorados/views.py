from django.shortcuts import render
from django.http import HttpResponse
from .models import Mentorados
from .models import Navigators
# Create your views here.

def mentorados (request):
    if request.method == "GET":
        navigators = Navigators.objects.all()
        return render(request, 'mentorados.html', {'estagios': Mentorados.estagio_choices, 'navigators': navigators})
    elif request.method == "POST":
        ...