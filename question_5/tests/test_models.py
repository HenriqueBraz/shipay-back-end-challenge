import sqlite3
from pathlib import Path

from app.models import UserModel


def create_test_database(database_path):
    schema_path = Path(__file__).resolve().parents[1] / "data" / "schema.sql"

    connection = sqlite3.connect(database_path)
    connection.executescript(schema_path.read_text())
    connection.close()


def test_create_user(tmp_path):
    database_path = tmp_path / "test.db"

    schema_path = Path(__file__).resolve().parents[1] / "data" / "schema.sql"

    connection = sqlite3.connect(database_path)
    connection.executescript(schema_path.read_text())
    connection.close()

    def test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    model = UserModel(test_connection)

    user_id = model.create_user(
        name="Joao Test",
        email="joao@test.com",
        password="hashed-password",
        role_id=2,
    )

    connection = test_connection()

    try:
        user = connection.execute(
            """
            SELECT id, name, email, password, role_id
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        assert user is not None
        assert user["name"] == "Joao Test"
        assert user["email"] == "joao@test.com"
        assert user["password"] == "hashed-password"
        assert user["role_id"] == 2

    finally:
        connection.close()


def test_role_exists(tmp_path):
    database_path = tmp_path / "test.db"

    create_test_database(database_path)

    def test_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    model = UserModel(test_connection)

    assert model.role_exists(2) is True
    assert model.role_exists(999) is False
