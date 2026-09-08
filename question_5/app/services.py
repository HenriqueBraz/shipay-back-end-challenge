import base64
import hashlib
import secrets
import string

from app.models import UserModel


class UserService:
    def __init__(self, user_model: UserModel):
        self._user_model = user_model

    def create_user(
        self,
        name: str,
        email: str,
        role_id: int,
        password: str | None = None,
    ) -> tuple[int, str]:

        if not self._user_model.role_exists(role_id):
            raise ValueError("Role not found.")

        if password is None:
            password = self._generate_password()

        password_hash = self._hash_password(password)

        user_id = self._user_model.create_user(
            name=name,
            email=email,
            password=password_hash,
            role_id=role_id,
        )

        return user_id, password

    @staticmethod
    def _generate_password(length: int = 12) -> str:
        characters = string.ascii_letters + string.digits

        return "".join(secrets.choice(characters) for _ in range(length))

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = secrets.token_bytes(16)

        password_hash = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=2**14,
            r=8,
            p=1,
        )

        encoded_salt = base64.b64encode(salt).decode("ascii")
        encoded_hash = base64.b64encode(password_hash).decode("ascii")

        return f"scrypt${encoded_salt}${encoded_hash}"
