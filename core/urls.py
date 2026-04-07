from django.urls import path
from .views import lista_empresas

urlpatterns = [
    path('', lista_empresas, name='lista_empresas'),
]