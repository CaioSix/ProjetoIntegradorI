#!/bin/sh
set -e

echo "==> Aplicando migrações..."
python manage.py migrate --noinput

echo "==> Carregando dados iniciais..."
python manage.py loaddata core/fixtures/dados_iniciais.json 2>/dev/null \
  && echo "Fixtures carregados." \
  || echo "AVISO: Fixtures já existem ou houve erro parcial — continuando."

echo "==> Criando superusuário..."
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password)
    print(f'Superusuario criado: {username}')
else:
    print(f'Superusuario ja existe: {username}')
"

echo "==> Iniciando servidor em 0.0.0.0:8000..."
exec python manage.py runserver 0.0.0.0:8000
