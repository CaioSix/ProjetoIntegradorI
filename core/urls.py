from django.urls import path
from .views import dashboard, lista_tarefas, todas_tarefas
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('tarefas/', todas_tarefas, name='todas_tarefas'),
    path('tarefas/<int:empresa_id>/', lista_tarefas, name='tarefas'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]