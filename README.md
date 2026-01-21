Desafio Fit - API de Livros (FastAPI)
=================================

API simples para cadastro de livros com autenticação JWT, documentação Swagger e boas práticas (camadas: router → service → repository).

Stack
-----
- Python 3.9
- FastAPI + Uvicorn
- SQLAlchemy 2.0 (sync)
- Alembic (migrations)
- SQLite (local)
- JWT (python-jose)
- Password hashing: passlib + bcrypt

Estrutura do Projeto (resumo)
-----------------------------
- app/main.py -> instancia FastAPI e registra routers
- app/config.py -> settings via env
- app/db/ -> engine, sessão, Base
- app/modules/auth/ -> login e validação JWT
- app/modules/books/ -> CRUD de livros (router/service/repository/model/schemas)
- migrations/ -> Alembic

Como rodar local (sem Docker)
-----------------------------
1) Criar venv e instalar deps
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2) Configurar .env
   Crie um arquivo .env na raiz:
   DATABASE_URL=sqlite:///./local.db
   JWT_SECRET_KEY=change-me
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRES_MIN=60

3) Rodar migrations
   alembic upgrade head

4) Subir a API
   uvicorn app.main:app --reload --reload-dir app

Acessos:
- Swagger: http://127.0.0.1:8000/docs


Autenticação (Login) - Como usar
--------------------------------
Usuário padrão (para simplificar o desafio):
- username: admin
- password: admin

1) Fazer login (pegar token)
   No Swagger, use: POST /auth/login
   Body:
   {
     "username": "admin",
     "password": "admin"
   }

   Resposta:
   {
     "access_token": "xxxxx.yyyyy.zzzzz",
     "token_type": "bearer"
   }

2) Usar token no Swagger
   - Clique em "Authorize" no topo do Swagger
   - Cole:
     Bearer SEU_TOKEN_AQUI
   - Autorize

Agora você consegue chamar endpoints protegidos.


Endpoints principais
-------------------
- POST /auth/login -> gera JWT
- GET /books -> lista livros
- POST /books -> cria livro
- GET /books/{id} -> detalhes
- PATCH /books/{id} -> atualiza
- DELETE /books/{id} -> remove


Modelo de Livro
---------------
- title (string)
- author (string)
- date_publish (YYYY-MM-DD, opcional)
- cover_url (URL da capa, opcional)

Exemplo:
{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "date_publish": "2008-08-01",
  "cover_url": "https://exemplo.com/capa.jpg"
}


Rodar testes
------------
pytest -q


Notas (dependências bcrypt/passlib)
----------------------------------
Se ocorrer erro de compatibilidade do bcrypt/passlib, fixe as versões:
- passlib==1.7.4
- bcrypt==3.2.2
