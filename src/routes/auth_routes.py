from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.dtos.auth_dto import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse
)
from src.controllers.auth_controller import register_user, login_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    return register_user(user, db)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return login_user(user, db)