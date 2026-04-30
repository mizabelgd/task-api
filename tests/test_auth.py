import pytest
from tests.conftest import auth_headers, register


class TestRegister:
    def test_success(self, client):
        r = client.post(
            "/api/v1/auth/register",
            json={"email": "new@test.com", "password": "password123"},
        )
        assert r.status_code == 201
        body = r.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_duplicate_email(self, client):
        payload = {"email": "dup@test.com", "password": "password123"}
        client.post("/api/v1/auth/register", json=payload)
        r = client.post("/api/v1/auth/register", json=payload)
        assert r.status_code == 409

    def test_invalid_email(self, client):
        r = client.post(
            "/api/v1/auth/register",
            json={"email": "not-an-email", "password": "password123"},
        )
        assert r.status_code == 422

    def test_missing_password(self, client):
        r = client.post("/api/v1/auth/register", json={"email": "nopass@test.com"})
        assert r.status_code == 422

    def test_error_is_problem_json(self, client):
        payload = {"email": "pjson@test.com", "password": "password123"}
        client.post("/api/v1/auth/register", json=payload)
        r = client.post("/api/v1/auth/register", json=payload)
        body = r.json()
        assert "type" in body
        assert "title" in body
        assert "status" in body
        assert body["status"] == 409


class TestLogin:
    def test_success(self, client):
        register(client, "login@test.com")
        r = client.post(
            "/api/v1/auth/login",
            data={"username": "login@test.com", "password": "password123"},
        )
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_wrong_password(self, client):
        register(client, "wrongpass@test.com")
        r = client.post(
            "/api/v1/auth/login",
            data={"username": "wrongpass@test.com", "password": "errada"},
        )
        assert r.status_code == 401

    def test_unknown_email(self, client):
        r = client.post(
            "/api/v1/auth/login",
            data={"username": "ghost@test.com", "password": "password123"},
        )
        assert r.status_code == 401

    def test_case_insensitive_email(self, client):
        register(client, "case@test.com")
        r = client.post(
            "/api/v1/auth/login",
            data={"username": "CASE@TEST.COM", "password": "password123"},
        )
        assert r.status_code == 200
