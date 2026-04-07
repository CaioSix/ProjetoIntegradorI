from django.shortcuts import render
from .models import Empresa

def lista_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, 'core/lista_empresas.html', {'empresas': empresas})