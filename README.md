# Sistema de Controle Operacional Contábil

Sistema full stack para gestão de tarefas contábeis — Projeto Integrador I, UNIVESP.

## Como rodar

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e Docker Compose instalados.

### Subir tudo com um comando

```bash
docker compose up --build
```

Na primeira execução, o backend aplica migrações, carrega os dados iniciais e cria o superusuário automaticamente.

| Serviço   | URL                              |
|-----------|----------------------------------|
| Frontend  | http://localhost:3000            |
| Backend   | http://localhost:8000/api/       |
| Swagger   | http://localhost:8000/api/docs/  |
| Admin     | http://localhost:8000/admin/     |

Login padrão: **admin** / **admin123**

---

## Estrutura do projeto

```
ProjetoNotaFiscal/
├── config/             # Configurações Django (settings, urls, wsgi)
├── core/               # App principal
│   ├── models.py       # Empresa, Competencia, Obrigacao, Tarefa
│   ├── api_views.py    # ViewSets + views de dashboard/pendentes
│   ├── serializers.py  # Serializers DRF
│   ├── signals.py      # Auto-criação de tarefas ao criar empresa
│   └── fixtures/       # Dados iniciais
├── frontend/           # Aplicação React
│   ├── src/
│   │   ├── api/        # Cliente HTTP centralizado
│   │   ├── components/ # Navbar, StatusBadge, PrazoTag, Modal
│   │   └── pages/      # Login, Dashboard, Tarefas, Empresas, Obrigacoes
│   ├── nginx.conf      # Proxy /api/ → backend
│   └── Dockerfile      # Build multi-stage (Node → nginx)
├── Dockerfile          # Backend Python
├── entrypoint.sh       # Migrações + fixtures + superuser + runserver
├── docker-compose.yml
└── requirements.txt
```

---

## Containers

| Container           | Porta  | Descrição                                    |
|---------------------|--------|----------------------------------------------|
| `contabil_backend`  | 8000   | Django 6 + DRF + Knox auth + SQLite          |
| `contabil_frontend` | 3000   | React 18 (build estático servido por nginx)  |

O nginx do frontend faz proxy de `/api/` para `backend:8000`, eliminando CORS.

---

## Variáveis de ambiente (backend)

| Variável                    | Padrão          | Descrição                         |
|-----------------------------|-----------------|-----------------------------------|
| `DJANGO_SECRET_KEY`         | chave insegura  | Chave secreta do Django           |
| `DJANGO_DEBUG`              | `True`          | Modo debug                        |
| `DJANGO_ALLOWED_HOSTS`      | `*`             | Hosts permitidos (`*` = todos)    |
| `DATABASE_PATH`             | `db.sqlite3`    | Caminho do arquivo SQLite         |
| `DJANGO_SUPERUSER_USERNAME` | `admin`         | Usuário administrador             |
| `DJANGO_SUPERUSER_PASSWORD` | `admin123`      | Senha do administrador            |

---

## Decisões técnicas

- **SQLite + volume Docker** — simples para uso acadêmico; dados persistem em `db_data` (volume nomeado).
- **Knox** — tokens com expiração, mais seguro que o token básico do DRF.
- **Signal `post_save` em Empresa** — ao criar uma empresa, tarefas da competência atual são geradas automaticamente com base no mapeamento `TipoEmpresaObrigacao`.
- **`pagination_class = None`** em Empresa/Competência/Obrigação — coleções pequenas retornam lista plana (sem envoltório paginado).
- **Nginx proxy** — frontend em porta 3000 proxia `/api/` para backend, sem CORS.
- **Runserver** — servidor de desenvolvimento Django; adequado para ambiente acadêmico.

### Limitação conhecida
A `TarefaSerializer` não retorna o campo `competencia` na listagem. A coluna não aparece na tabela de tarefas, mas o filtro por competência funciona normalmente via query param.

---

## Desenvolvimento local (sem Docker)

```bash
# Backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata core/fixtures/dados_iniciais.json
python manage.py createsuperuser
python manage.py runserver

# Frontend (outro terminal)
cd frontend
npm install
npm run dev   # proxy para localhost:8000 já configurado no vite.config.js
```
