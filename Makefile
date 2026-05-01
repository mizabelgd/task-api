.PHONY: install dev test build up down logs

install:
	uv sync

dev:
	uv run uvicorn app.main:app --reload

test:
	uv run pytest -v

build:
	docker build -t task-api .

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f api
