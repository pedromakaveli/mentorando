from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def mentorados (request):
    return HttpResponse("Estou no mentorado")