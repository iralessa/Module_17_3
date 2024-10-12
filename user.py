from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    stmt = select(User)  # выборка всех пользователей
    result = db.scalars(stmt).all()  # Получаем список всех пользователей
    return result  # Возвращаем список пользователей


@router.get('/user_id')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(User).where(User.user_id == user_id)  # выборка пользователя по user_id
    result = db.scalars(stmt).first()  # Получаем одного пользователя

    if result is not None:
        return result  # Возвращаем пользователя, если он найден
        # Если пользователь не найден, выбрасываем исключение
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="пользователь не найден")

@router.post('/create')
async def create_user(user_data: CreateUser, db: Annotated[Session, Depends(get_db)]):
    slug_value = user_data.username
    db.execute(insert(User).values(username=user_data.username, firstname=user_data.firstname,
                                   lastname=user_data.lastname, age=user_data.age, slug= slug_value))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put('/update')
async def update_user(user_id: int, user_data: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    stmt = select(User).where(User.id == user_id)
    user = db.scalars(stmt).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден.")

    stmt = update(User).where(User.id == user_id).values(
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        age=user_data.age
    )
    db.execute(stmt)
    db.commit()

    return {'message': 'Обновление пользователя прошло успешно.'}


@router.delete('/delete')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = select(User).where(User.id == user_id)
    user = db.scalars(stmt).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден.")

    stmt = delete(User).where(User.id == user_id)
    db.execute(stmt)
    db.commit()

    return {'message': 'Удаление пользователя прошло успешно.'}