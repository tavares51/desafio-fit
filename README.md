DESAFIO FIT - API DE LIVROS (FASTAPI)
================================

API REST para cadastro de livros com autenticação JWT, seguindo boas práticas
de arquitetura (Clean Code, SOLID, separação de camadas) e pronta para rodar
localmente, com Docker ou Docker Compose.

--------------------------------------------------
VISÃO GERAL
--------------------------------------------------
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL local (banco) + Supabase (storage)
- JWT simples (Bearer Token)
- Swagger / OpenAPI automático
- Arquitetura em camadas (router, service, repository)

--------------------------------------------------
ESTRUTURA DO PROJETO
--------------------------------------------------
app/ <br>
├── main.py            -> Inicialização da aplicação <br>
├── config.py          -> Configurações (env) <br>
├── db/                -> Engine, sessão e Base <br>
├── common/            -> Segurança, JWT, utilitários <br>
├── modules/ <br>
├──   ├── auth/          -> Login e geração de token <br>
├──   └── books/         -> CRUD de livros <br>
migrations/            -> Alembic (migrations) <br>
Dockerfile <br>
docker-compose.yml <br>
requirements.txt

--------------------------------------------------
MODELO DE LIVRO
--------------------------------------------------
- title (string)
- author (string)
- date_publish (YYYY-MM-DD, opcional)
- cover_url (URL da capa, opcional)

--------------------------------------------------
PRÉ-REQUISITO (BANCO LOCAL)
--------------------------------------------------
- PostgreSQL instalado e em execução
- Banco criado (desafio_fit)
- Usuário com acesso

Usuário padrão (postgres):
- Garanta o role e senha:
  createuser -s postgres
  psql -d postgres -c "ALTER USER postgres WITH PASSWORD 'postgres';"
- DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/desafio_fit?sslmode=disable
- DB_USER=postgres
- DB_PASSWORD=postgres

Exemplo (psql):
CREATE DATABASE desafio_fit;

RODAR LOCAL (SEM DOCKER)
--------------------------------------------------
1) Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

2) Instalar dependências
pip install -r requirements.txt

3) Ajustar .env
- DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/desafio_fit?sslmode=disable
- SUPABASE_URL / SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY para storage

4) Aplicar migrations
alembic upgrade head

5) Subir a API
uvicorn app.main:app --reload --reload-dir app

Swagger:
http://127.0.0.1:8000/docs

--------------------------------------------------
AUTENTICAÇÃO (LOGIN)
--------------------------------------------------
Endpoint:
POST /auth/login

Payload:
{
  "username": "admin",
  "password": "admin"
}

Resposta:
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}

No Swagger:
- Clique em Authorize
- Cole: Bearer <token>

--------------------------------------------------
ENDPOINTS PRINCIPAIS
--------------------------------------------------
POST   /auth/login
GET    /books
POST   /books
GET    /books/{id}
PATCH  /books/{id}
DELETE /books/{id}
POST   /books/{id}/cover

--------------------------------------------------
RODAR COM DOCKER
--------------------------------------------------
Build da imagem:
docker build -t desafio-fit-api .

Rodar container:
docker run -p 8000:8000 --env-file .env desafio-fit-api

Obs: se usar Postgres local fora do container, troque o host para
`host.docker.internal`:
- DATABASE_URL=postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/desafio_fit?sslmode=disable

--------------------------------------------------
RODAR COM DOCKER COMPOSE
--------------------------------------------------
Subir serviços (API + Postgres):
docker compose up --build

Obs: não precisa de Postgres instalado na máquina.

Aplicar migrations:
docker compose exec api alembic upgrade head

--------------------------------------------------
BOAS PRÁTICAS APLICADAS
--------------------------------------------------
- Separação de responsabilidades
- JWT simples 
- Versionamento de banco com Alembic
- Swagger automático
- Projeto pronto para deploy

--------------------------------------------------
OBSERVAÇÕES
--------------------------------------------------
O projeto foi desenvolvido com foco em clareza, simplicidade e padrão
profissional, sendo adequado para avaliações técnicas e expansão futura.
