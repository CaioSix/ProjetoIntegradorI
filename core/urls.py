from django.urls import path
from .views import dashboard, lista_tarefas

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('tarefas/<int:empresa_id>/', lista_tarefas, name='tarefas')
]