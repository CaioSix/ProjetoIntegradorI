from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import dashboard, lista_tarefas, todas_tarefas
from .api_views import (
    EmpresaViewSet,
    CompetenciaViewSet,
    ObrigacaoViewSet,
    TarefaViewSet,
    LoginView,
    dashboard_api,
    tarefas_pendentes,
)
from django.contrib.auth import views as auth_views
from knox import views as knox_views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'competencias', CompetenciaViewSet)
router.register(r'obrigacoes', ObrigacaoViewSet)
router.register(r'tarefas', TarefaViewSet)

urlpatterns = [
    # path('', dashboard, name='dashboard'),
    # path('tarefas/', todas_tarefas, name='todas_tarefas'),
    # path('tarefas/<int:empresa_id>/', lista_tarefas, name='tarefas'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/dashboard/', dashboard_api),
    path('api/tarefas/pendentes/', tarefas_pendentes),
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', knox_views.LogoutView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]