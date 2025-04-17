from fastapi import APIRouter, Body, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database.database import get_session
from models.crud.user import create_user, get_by_email, get_all_users
from models.User import User
from typing import List


router = APIRouter()


@router.post("/signup")
async def signup(username: str, password: str, session: Session = Depends(get_session)) -> dict:
    """
    Регистрирует нового пользователя с указанными username и password.
    """
    # Проверяем, не существует ли пользователь с таким username (email)
    existing_user = get_by_email(session, username)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username already exists"
        )

    # Создаём пользователя
    create_user(session, username, password)
    return {"message": "User successfully registered"}

@router.post("/signin")
async def signin(username: str, password: str, session: Session = Depends(get_session)) -> dict:
    """
    Авторизует пользователя по username и password.
    """
    user = get_by_email(session, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    # Проверяем пароль
    if not user.check_password(password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )
    return {"message": "User signed in successfully"}

@router.get("/users", response_model=List[User])
async def get_users(session: Session = Depends(get_session)):
    """
    Возвращает список всех пользователей.
    """
    return get_all_users(session)