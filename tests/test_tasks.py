import pytest
from tests.conftest import auth_headers, register

TASK_URL = "/api/v1/tasks"


@pytest.fixture()
def headers(client):
    register(client, "owner@test.com")
    return auth_headers(client, "owner@test.com")


def create_task(client, headers, title="Tarefa", **kwargs):
    return client.post(TASK_URL, json={"title": title, **kwargs}, headers=headers)


class TestCreateTask:
    def test_success(self, client, headers):
        r = create_task(client, headers, title="Nova tarefa", description="Desc", status="pending")
        assert r.status_code == 201
        body = r.json()
        assert body["title"] == "Nova tarefa"
        assert body["status"] == "pending"
        assert "id" in body
        assert "user_id" in body

    def test_unauthenticated(self, client):
        r = client.post(TASK_URL, json={"title": "Sem token"})
        assert r.status_code == 401

    def test_invalid_token(self, client):
        r = client.post(
            TASK_URL,
            json={"title": "Token inválido"},
            headers={"Authorization": "Bearer token.invalido.aqui"},
        )
        assert r.status_code == 401

    def test_missing_title(self, client, headers):
        r = client.post(TASK_URL, json={"description": "Sem título"}, headers=headers)
        assert r.status_code == 422

    def test_invalid_status(self, client, headers):
        r = create_task(client, headers, title="Status errado", status="invalido")
        assert r.status_code == 422


class TestListTasks:
    def test_returns_pagination_envelope(self, client, headers):
        create_task(client, headers, title="T1")
        create_task(client, headers, title="T2")
        r = client.get(TASK_URL, headers=headers)
        assert r.status_code == 200
        body = r.json()
        assert body["total"] == 2
        assert body["skip"] == 0
        assert body["limit"] == 20
        assert len(body["items"]) == 2

    def test_pagination_skip_limit(self, client, headers):
        for i in range(5):
            create_task(client, headers, title=f"T{i}")
        r = client.get(f"{TASK_URL}?skip=2&limit=2", headers=headers)
        body = r.json()
        assert body["total"] == 5
        assert len(body["items"]) == 2

    def test_empty_list(self, client, headers):
        r = client.get(TASK_URL, headers=headers)
        body = r.json()
        assert body["total"] == 0
        assert body["items"] == []

    def test_unauthenticated(self, client):
        assert client.get(TASK_URL).status_code == 401

    def test_only_own_tasks(self, client, headers):
        create_task(client, headers, title="Minha tarefa")

        register(client, "other@test.com")
        other_headers = auth_headers(client, "other@test.com")
        create_task(client, other_headers, title="Tarefa do outro")

        r = client.get(TASK_URL, headers=headers)
        assert r.json()["total"] == 1


class TestGetTask:
    def test_success(self, client, headers):
        task_id = create_task(client, headers, title="Buscar").json()["id"]
        r = client.get(f"{TASK_URL}/{task_id}", headers=headers)
        assert r.status_code == 200
        assert r.json()["title"] == "Buscar"

    def test_not_found(self, client, headers):
        r = client.get(f"{TASK_URL}/99999", headers=headers)
        assert r.status_code == 404

    def test_other_user_gets_404(self, client, headers):
        task_id = create_task(client, headers, title="Privada").json()["id"]

        register(client, "spy@test.com")
        spy = auth_headers(client, "spy@test.com")

        assert client.get(f"{TASK_URL}/{task_id}", headers=spy).status_code == 404

    def test_unauthenticated(self, client):
        assert client.get(f"{TASK_URL}/1").status_code == 401


class TestUpdateTask:
    def test_partial_update_status(self, client, headers):
        task_id = create_task(client, headers, title="Atualizar").json()["id"]
        r = client.patch(f"{TASK_URL}/{task_id}", json={"status": "done"}, headers=headers)
        assert r.status_code == 200
        assert r.json()["status"] == "done"

    def test_partial_update_title(self, client, headers):
        task_id = create_task(client, headers, title="Antigo").json()["id"]
        r = client.patch(f"{TASK_URL}/{task_id}", json={"title": "Novo"}, headers=headers)
        assert r.status_code == 200
        assert r.json()["title"] == "Novo"

    def test_not_found(self, client, headers):
        r = client.patch(f"{TASK_URL}/99999", json={"status": "done"}, headers=headers)
        assert r.status_code == 404

    def test_other_user_gets_404(self, client, headers):
        task_id = create_task(client, headers, title="Protegida").json()["id"]

        register(client, "attacker@test.com")
        attacker = auth_headers(client, "attacker@test.com")

        r = client.patch(f"{TASK_URL}/{task_id}", json={"status": "done"}, headers=attacker)
        assert r.status_code == 404

    def test_unauthenticated(self, client):
        assert client.patch(f"{TASK_URL}/1", json={"status": "done"}).status_code == 401


class TestDeleteTask:
    def test_success(self, client, headers):
        task_id = create_task(client, headers, title="Deletar").json()["id"]
        r = client.delete(f"{TASK_URL}/{task_id}", headers=headers)
        assert r.status_code == 204
        assert client.get(f"{TASK_URL}/{task_id}", headers=headers).status_code == 404

    def test_not_found(self, client, headers):
        assert client.delete(f"{TASK_URL}/99999", headers=headers).status_code == 404

    def test_other_user_gets_404(self, client, headers):
        task_id = create_task(client, headers, title="Intocável").json()["id"]

        register(client, "deleter@test.com")
        deleter = auth_headers(client, "deleter@test.com")

        assert client.delete(f"{TASK_URL}/{task_id}", headers=deleter).status_code == 404

    def test_unauthenticated(self, client):
        assert client.delete(f"{TASK_URL}/1").status_code == 401


class TestErrorFormat:
    def test_404_is_problem_json(self, client, headers):
        r = client.get(f"{TASK_URL}/99999", headers=headers)
        body = r.json()
        assert body["status"] == 404
        assert "type" in body
        assert "title" in body
        assert "instance" in body
