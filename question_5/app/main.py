# This is the main entry point for the FastAPI application.
# uvicorn app.main:app --reload

# swagger docs: http://
# http://127.0.0.1:8000/docs

# ---------------------------------------------------------------------------------------

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from app.models import UserModel
from app.schemas import UserCreate
from app.services import UserService

app = FastAPI(title="Shipay - User API")


def get_user_service() -> UserService:
    return UserService(UserModel())


@app.post("/users", status_code=201)
def create_user(
    user: UserCreate,
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> dict:
    try:
        user_id, password = user_service.create_user(
            name=user.name,
            email=user.email,
            role_id=user.role_id,
            password=user.password,
        )

        return {
            "id": user_id,
            "name": user.name,
            "email": user.email,
            "role_id": user.role_id,
            "password": password,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error
