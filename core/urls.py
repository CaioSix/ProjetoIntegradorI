from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import dashboard, lista_tarefas, todas_tarefas
from .api_views import (
    EmpresaViewSet,
    CompetenciaViewSet,
    ObrigacaoViewSet,
    TarefaViewSet,
    dashboard_api,
    tarefas_geral
)
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'competencias', CompetenciaViewSet)
router.register(r'obrigacoes', ObrigacaoViewSet)
router.register(r'tarefas', TarefaViewSet)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('tarefas/', todas_tarefas, name='todas_tarefas'),
    path('tarefas/<int:empresa_id>/', lista_tarefas, name='tarefas'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/dashboard/', dashboard_api),
    path('api/tarefas_geral', tarefas_geral),
    path('api/', include(router.urls)),
]