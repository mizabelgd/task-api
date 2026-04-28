# task-api

Micro-API RESTful para gestão de tarefas, desenvolvida como MVP para a disciplina de Engenharia de Software e IA.

## Objetivo

Fornecer uma API simples e extensível para criação, leitura, atualização e remoção de tarefas (CRUD), servindo como base para estudos de arquitetura de APIs com boas práticas de desenvolvimento.

## Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.13+ |
| Framework | FastAPI |
| Validação | Pydantic v2 |
| Banco de dados | PostgreSQL |
| ORM | SQLAlchemy + asyncpg |
| Servidor | Uvicorn |
| Gerenciador de pacotes | uv |
| Testes | Pytest + HTTPX |

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
  │  SQL (asyncpg / SQLAlchemy)
  ▼
PostgreSQL
```

Diagrama de componentes completo: [docs/architecture.md](docs/architecture.md).

## Como rodar localmente

**Pré-requisitos:** Python 3.13+ e [uv](https://docs.astral.sh/uv/) instalados.

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

# 4. Rode a API
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.
Documentação interativa: `http://localhost:8000/docs`.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Verifica status da API |
| GET | `/tasks` | Lista todas as tarefas |
| POST | `/tasks` | Cria uma nova tarefa |
| GET | `/tasks/{id}` | Retorna uma tarefa pelo ID |
| PUT | `/tasks/{id}` | Atualiza uma tarefa |
| DELETE | `/tasks/{id}` | Remove uma tarefa |

## Roadmap

### v0.1.0 — MVP (atual)
- [x] Estrutura base do projeto com FastAPI
- [x] Endpoint `GET /health`
- [x] Diagrama de componentes (docs/architecture.md)
- [ ] Estrutura de camadas
  - [ ] `app/api/` — routers (controllers)
  - [ ] `app/services/` — lógica de negócio
  - [ ] `app/repositories/` — acesso ao banco
  - [ ] `app/models/` — modelos SQLAlchemy
  - [ ] `app/schemas/` — schemas Pydantic
- [ ] Integração com PostgreSQL via SQLAlchemy + asyncpg
- [ ] Migrações com Alembic
- [ ] CRUD completo de tarefas (`/tasks`)
  - [ ] `POST /tasks` — criar tarefa
  - [ ] `GET /tasks` — listar tarefas
  - [ ] `GET /tasks/{id}` — buscar por ID
  - [ ] `PUT /tasks/{id}` — atualizar tarefa
  - [ ] `DELETE /tasks/{id}` — remover tarefa
- [ ] Validação de dados com Pydantic
- [ ] Documentação automática via Swagger UI

### v0.2.0 — Qualidade
- [ ] Cobertura de testes com Pytest + HTTPX
- [ ] CI com GitHub Actions
- [ ] Tratamento de erros padronizado (RFC 7807)
- [ ] Paginação na listagem de tarefas

### v1.0.0 — Produção
- [ ] Autenticação com JWT
- [ ] Rate limiting
- [ ] Deploy containerizado com Docker
