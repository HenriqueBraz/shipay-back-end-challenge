import sqlite3
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app, get_user_service
from app.models import UserModel
from app.services import UserService


def create_test_database(database_path):
    schema_path = Path(__file__).resolve().parents[1] / "data" / "schema.sql"

    connection = sqlite3.connect(database_path)
    connection.executescript(schema_path.read_text())
    connection.close()


def create_test_service(database_path):
    def test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    user_model = UserModel(test_connection)

    return UserService(user_model)


def create_test_client(database_path):
    create_test_database(database_path)

    test_service = create_test_service(database_path)

    app.dependency_overrides[get_user_service] = lambda: test_service

    return TestClient(app)


def test_create_user_api(tmp_path):
    database_path = tmp_path / "test.db"
    client = create_test_client(database_path)

    try:
        response = client.post(
            "/users",
            json={
                "name": "João Test",
                "email": "joao@test.com",
                "role_id": 2,
                "password": "MinhaSenha123",
            },
        )

        assert response.status_code == 201

        data = response.json()

        assert data["name"] == "João Test"
        assert data["email"] == "joao@test.com"
        assert data["role_id"] == 2
        assert data["password"] == "MinhaSenha123"

        connection = sqlite3.connect(database_path)

        try:
            user = connection.execute(
                """
                SELECT password
                FROM users
                WHERE id = ?
                """,
                (data["id"],),
            ).fetchone()

            assert user is not None
            assert user[0].startswith("scrypt$")
            assert user[0] != "MinhaSenha123"

        finally:
            connection.close()

    finally:
        app.dependency_overrides.clear()


def test_create_user_api_without_password(tmp_path):
    database_path = tmp_path / "test.db"
    client = create_test_client(database_path)

    try:
        response = client.post(
            "/users",
            json={
                "name": "João Generated",
                "email": "generated@test.com",
                "role_id": 2,
            },
        )

        assert response.status_code == 201

        data = response.json()

        assert data["name"] == "João Generated"
        assert data["email"] == "generated@test.com"
        assert data["role_id"] == 2
        assert data["password"] is not None
        assert len(data["password"]) == 12

        connection = sqlite3.connect(database_path)

        try:
            user = connection.execute(
                """
                SELECT password
                FROM users
                WHERE id = ?
                """,
                (data["id"],),
            ).fetchone()

            assert user is not None
            assert user[0].startswith("scrypt$")
            assert user[0] != data["password"]

        finally:
            connection.close()

    finally:
        app.dependency_overrides.clear()


def test_create_user_api_with_invalid_role(tmp_path):
    database_path = tmp_path / "test.db"
    client = create_test_client(database_path)

    try:
        response = client.post(
            "/users",
            json={
                "name": "Invalid Role",
                "email": "invalid@test.com",
                "role_id": 999,
                "password": "MinhaSenha123",
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Role not found."

    finally:
        app.dependency_overrides.clear()


def test_create_user_api_with_missing_email(tmp_path):
    database_path = tmp_path / "test.db"
    client = create_test_client(database_path)

    try:
        response = client.post(
            "/users",
            json={
                "name": "João Missing Email",
                "role_id": 2,
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()
