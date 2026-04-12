from django.urls import path
from .views import dashboard, lista_tarefas, todas_tarefas

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('tarefas/', todas_tarefas, name='todas_tarefas'),
    path('tarefas/<int:empresa_id>/', lista_tarefas, name='tarefas'),
]