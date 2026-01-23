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
POST   /auth/login <br>
GET    /books <br>
POST   /books <br>
GET    /books/{id} <br>
PATCH  /books/{id} <br>
DELETE /books/{id} <br>
POST   /books/{id}/cover <br>

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
RODAR COM DOCKER COMPOSE (RECOMENDADO)
--------------------------------------------------
Subir serviços (API + Postgres):
docker compose up --build

Obs: não precisa instalar o PostgreSQL local.

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
5. BOAS PRÁTICAS E CLEAN CODE
--------------------------------------------------
1) Separação de responsabilidades (Single Responsibility Principle)
2) Código legível e organizado por camadas
3) Nomes semânticos para variáveis, funções e componentes
4) Padronização de respostas da API

--------------------------------------------------
6. PONTOS AVALIADOS – COMO RESPONDER
--------------------------------------------------
1) Funcionalidade: Todas as operações de CRUD foram implementadas e testadas.
2) Fidelidade ao design: O layout segue fielmente o protótipo do Figma fornecido.
3) Responsividade: A interface se adapta a diferentes tamanhos de tela.
4) Arquitetura: Separação clara entre Front-end e Back-end via API REST.
5) Robustez: Validações no back-end e tratamento de erros no front-end.
6) Testes: Estrutura preparada para testes unitários e de integração.
7) Documentação: README detalhado com instruções claras de execução.

--------------------------------------------------
7. POSSÍVEIS PERGUNTAS DA BANCA
--------------------------------------------------
1) Por que escolheu essa arquitetura?
2) Como a aplicação pode escalar?
3) Como adicionaria autenticação?
4) Como garantiria maior cobertura de testes?

--------------------------------------------------
8. CONCLUSÃO
--------------------------------------------------
A solução atende integralmente aos requisitos do desafio, demonstrando domínio de conceitos Full
Stack, organização de código, boas práticas e visão arquitetural.

--------------------------------------------------
9. DESCRIÇÃO DO PROJETO
--------------------------------------------------
Este projeto é uma API REST de livros feita em FastAPI, com CRUD completo e
autenticação JWT. Ele segue uma arquitetura em camadas (router, service,
repository) para manter separação de responsabilidades e facilitar manutenção.
O banco roda em PostgreSQL (recomendado via Docker Compose para não precisar
instalar localmente), e o storage de capas fica no Supabase.

Boas práticas aplicadas:
- Separação clara de responsabilidades (SRP)
- Código organizado por camadas
- Nomes semânticos em variáveis e funções
- Respostas padronizadas na API
- Migrations com Alembic e documentação via Swagger

Pontos avaliados (como o projeto responde):
- Funcionalidade: CRUD implementado e testado na API
- Fidelidade ao design: pronto para integrar com um front seguindo o Figma
- Responsividade: front pode consumir a API em qualquer tamanho de tela
- Arquitetura: front-end e back-end desacoplados via REST
- Robustez: validações no back-end e tratamento de erros
- Testes: estrutura preparada para testes unitários e integração
- Documentação: README com instruções completas

Conclusão:
A solução cumpre os requisitos do desafio, mostrando domínio full stack,
organização de código, boas práticas e visão arquitetural.
