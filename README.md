# task-api

Micro-API RESTful para gestão de tarefas, desenvolvida como MVP para a disciplina de Engenharia de Software e IA.

## Objetivo

Fornecer uma API simples e extensível para criação, leitura, atualização e remoção de tarefas (CRUD), servindo como base para estudos de arquitetura de APIs com boas práticas de desenvolvimento.

## Claude Code

Este projeto foi desenvolvido com o auxílio do [Claude Code](https://claude.ai/code), o agente de engenharia de software da Anthropic, integrado ao VS Code e utilizado diretamente no terminal — com revisão e direcionamento da desenvolvedora em cada etapa.

O agente foi usado ao longo de todas as versões:

- **Planejamento** — definição e refinamento do roadmap (v0.1.0 → v1.0.0) em conversas iterativas.
- **Geração de código** — criação e modificação de models, schemas, repositories, services e endpoints, sempre respeitando a arquitetura em camadas e o contexto existente.
- **Autenticação JWT** — implementação do fluxo de registro, login e proteção de rotas com `bcrypt` e `PyJWT`.
- **Testes** — criação da suíte Pytest com fixtures de banco isolado, cobertura de CRUD, autenticação, isolamento entre usuários e validação do formato RFC 7807.
- **Infraestrutura** — geração de `Dockerfile`, `docker-compose.yml`, `Makefile` e collection Postman.
- **Versionamento** — mensagens de commit no padrão convencional executadas ao final de cada versão.

> Em cada ciclo, o agente lia o estado atual do projeto, propunha as mudanças, executava, rodava os testes e fazia o commit — atuando como par de programação orientado por contexto e sob revisão contínua.

## Stack

| Camada                 | Tecnologia            |
| ---------------------- | --------------------- |
| Linguagem              | Python 3.13+          |
| Framework              | FastAPI               |
| Validação              | Pydantic v2           |
| Banco de dados         | PostgreSQL            |
| ORM                    | SQLAlchemy + psycopg2 |
| Servidor               | Uvicorn               |
| Gerenciador de pacotes | uv                    |
| Testes                 | Pytest + HTTPX        |

## Arquitetura

O backend segue uma arquitetura em três camadas:

```
Cliente
  │  HTTP/JSON (REST)
  ▼
TaskController  — recebe requisições e delega ao service
  │
TaskService     — implementa a lógica de negócio
  │
TaskRepository  — gerencia queries SQL contra o PostgreSQL
  │  SQL (psycopg2 / SQLAlchemy)
  ▼
PostgreSQL
```

Diagrama de componentes completo: [docs/architecture.md](docs/architecture.md).

## Como rodar localmente

**Pré-requisitos:** Python 3.13+, [uv](https://docs.astral.sh/uv/) e PostgreSQL instalados.

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd task-api

# 2. Crie e ative o ambiente virtual
uv venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 3. Instale as dependências
uv sync

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais do PostgreSQL

# 5. Rode a API (as tabelas são criadas automaticamente no startup)
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.
Documentação interativa: `http://localhost:8000/docs`.

## Endpoints

| Método | Rota                    | Auth | Descrição                        |
| ------ | ----------------------- | ---- | -------------------------------- |
| GET    | `/health`               | —    | Verifica status da API           |
| POST   | `/api/v1/auth/register` | —    | Cria conta e retorna JWT         |
| POST   | `/api/v1/auth/login`    | —    | Autentica e retorna JWT          |
| GET    | `/api/v1/tasks`         | JWT  | Lista tarefas do usuário         |
| POST   | `/api/v1/tasks`         | JWT  | Cria uma nova tarefa             |
| GET    | `/api/v1/tasks/{id}`    | JWT  | Retorna uma tarefa pelo ID       |
| PATCH  | `/api/v1/tasks/{id}`    | JWT  | Atualiza parcialmente uma tarefa |
| DELETE | `/api/v1/tasks/{id}`    | JWT  | Remove uma tarefa                |

## Docker

Para subir a API e o banco com um único comando:

```bash
cp .env.example .env   # ajuste SECRET_KEY antes de subir
make up                # docker compose up -d --build
make logs              # acompanhar logs da API
make down              # parar e remover containers
```

> O `docker-compose.yml` já configura `DATABASE_URL` apontando para o serviço `db` interno.

## Makefile

| Comando       | Descrição                          |
| ------------- | ---------------------------------- |
| `make install`| Instala dependências (`uv sync`)   |
| `make dev`    | Sobe a API em modo reload          |
| `make test`   | Executa os testes                  |
| `make build`  | Builda a imagem Docker             |
| `make up`     | Sobe os containers em background   |
| `make down`   | Para e remove os containers        |
| `make logs`   | Exibe logs da API em tempo real    |

## Postman

A collection está em [docs/task-api.postman_collection.json](docs/task-api.postman_collection.json).

**Como importar:**

1. Abra o Postman → **Import** → selecione o arquivo acima.
2. A collection já inclui uma variável `base_url` apontando para `http://localhost:8000`.
3. Execute **POST /auth/register** ou **POST /auth/login** — o token JWT é salvo automaticamente na variável `token` via script de teste.
4. Todas as requisições de tasks já usam `Bearer {{token}}`, então basta chamar normalmente após autenticar.

> Para apontar para outro ambiente, edite `base_url` em **Collection → Variables**.

## Roadmap

### v0.1.0 — MVP

- [x] Estrutura base do projeto com FastAPI
- [x] Endpoint `GET /health`
- [x] Diagrama de componentes (docs/architecture.md)
- [x] Estrutura de camadas
  - [x] `app/api/` — routers (controllers)
  - [x] `app/services/` — lógica de negócio
  - [x] `app/repositories/` — acesso ao banco
  - [x] `app/models/` — modelos SQLAlchemy
  - [x] `app/schemas/` — schemas Pydantic
- [x] Integração com PostgreSQL via SQLAlchemy + psycopg2
- [x] Criação automática de tabelas no startup (`create_all`)
- [x] CRUD completo de tarefas (`/api/v1/tasks`)
  - [x] `POST /api/v1/tasks` — criar tarefa
  - [x] `GET /api/v1/tasks` — listar tarefas
  - [x] `GET /api/v1/tasks/{id}` — buscar por ID
  - [x] `PATCH /api/v1/tasks/{id}` — atualizar tarefa parcialmente
  - [x] `DELETE /api/v1/tasks/{id}` — remover tarefa
- [x] Validação de dados com Pydantic v2
- [x] Documentação automática via Swagger UI (`/docs`)

### v0.2.0 — Autenticação

- [x] Autenticação com JWT (registro, login e proteção de rotas)
- [x] Associação de tarefas ao usuário autenticado
- [x] Tratamento de erros padronizado (RFC 7807)

### v0.3.0 — Qualidade

- [x] Cobertura de testes com Pytest + HTTPX
  - [x] Testes de endpoints CRUD de tarefas
  - [x] Testes de registro e login
  - [x] Testes de rotas protegidas (com e sem token)
  - [x] Testes de isolamento entre usuários
  - [x] Testes do formato de erro RFC 7807
- [x] Paginação na listagem de tarefas (`items`, `total`, `skip`, `limit`)

### v1.0.0 — Produção (atual)

- [x] Rate limiting nos endpoints de autenticação (10 req/min via slowapi)
- [x] Deploy containerizado com Docker (`Dockerfile` + `docker-compose.yml`)
- [x] Makefile com atalhos para dev, testes e Docker
