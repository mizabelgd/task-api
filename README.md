# task-api

Micro-API RESTful para gestão de tarefas, desenvolvida como MVP para a disciplina de Engenharia de Software e IA.

## Objetivo

Fornecer uma API simples e extensível para criação, leitura, atualização e remoção de tarefas (CRUD), servindo como base para estudos de arquitetura de APIs com boas práticas de desenvolvimento.

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

| Método | Rota                 | Descrição                        |
| ------ | -------------------- | -------------------------------- |
| GET    | `/health`            | Verifica status da API           |
| GET    | `/api/v1/tasks`      | Lista todas as tarefas           |
| POST   | `/api/v1/tasks`      | Cria uma nova tarefa             |
| GET    | `/api/v1/tasks/{id}` | Retorna uma tarefa pelo ID       |
| PATCH  | `/api/v1/tasks/{id}` | Atualiza parcialmente uma tarefa |
| DELETE | `/api/v1/tasks/{id}` | Remove uma tarefa                |

## Roadmap

### v0.1.0 — MVP (atual)

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

- [ ] Autenticação com JWT (registro, login e proteção de rotas)
- [ ] Associação de tarefas ao usuário autenticado
- [ ] Tratamento de erros padronizado (RFC 7807)

### v0.3.0 — Qualidade

- [ ] Cobertura de testes com Pytest + HTTPX
  - [ ] Testes de endpoints CRUD de tarefas
  - [ ] Testes de registro e login
  - [ ] Testes de rotas protegidas (com e sem token)
- [ ] Paginação na listagem de tarefas

### v1.0.0 — Produção

- [ ] Rate limiting
- [ ] Deploy containerizado com Docker
- [ ] Criar Makefile
