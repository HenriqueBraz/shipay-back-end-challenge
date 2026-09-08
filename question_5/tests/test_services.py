import sqlite3
from pathlib import Path

import pytest

from app.models import UserModel
from app.services import UserService


def create_test_database(database_path):
    schema_path = Path(__file__).resolve().parents[1] / "data" / "schema.sql"

    connection = sqlite3.connect(database_path)
    connection.executescript(schema_path.read_text())
    connection.close()


def create_service(database_path):
    def test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    user_model = UserModel(test_connection)

    return UserService(user_model)


def test_create_user_with_password(tmp_path):
    database_path = tmp_path / "test.db"

    create_test_database(database_path)
    service = create_service(database_path)

    user_id, password = service.create_user(
        name="João Test",
        email="joao@test.com",
        role_id=2,
        password="MinhaSenha123",
    )

    connection = sqlite3.connect(database_path)

    try:
        user = connection.execute(
            """
            SELECT password
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        assert password == "MinhaSenha123"
        assert user is not None
        assert user[0] != "MinhaSenha123"

    finally:
        connection.close()


def test_create_user_without_password(tmp_path):
    database_path = tmp_path / "test.db"

    create_test_database(database_path)
    service = create_service(database_path)

    user_id, password = service.create_user(
        name="João Generated",
        email="generated@test.com",
        role_id=2,
    )

    connection = sqlite3.connect(database_path)

    try:
        user = connection.execute(
            """
            SELECT password
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        assert password is not None
        assert user[0].startswith("scrypt$")
        assert user is not None
        assert user[0] != password

    finally:
        connection.close()


def test_create_user_with_invalid_role(tmp_path):
    database_path = tmp_path / "test.db"

    create_test_database(database_path)
    service = create_service(database_path)

    with pytest.raises(ValueError, match="Role not found."):
        service.create_user(
            name="Invalid Role",
            email="invalid@test.com",
            role_id=999,
            password="MinhaSenha123",
        )
