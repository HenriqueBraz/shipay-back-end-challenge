from app.database import get_connection


class UserModel:
    def __init__(self, get_connection_func=get_connection):
        self._get_connection = get_connection_func

    def role_exists(self, role_id: int) -> bool:
        connection = self._get_connection()

        try:
            role = connection.execute(
                """
                SELECT 1
                FROM roles
                WHERE id = ?
                """,
                (role_id,),
            ).fetchone()

            return role is not None

        finally:
            connection.close()

    def create_user(
        self,
        name: str,
        email: str,
        password: str,
        role_id: int,
    ) -> int:
        connection = self._get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO users (
                    name,
                    email,
                    password,
                    role_id,
                    created_at
                )
                VALUES (?, ?, ?, ?, DATE('now'))
                """,
                (name, email, password, role_id),
            )

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()
