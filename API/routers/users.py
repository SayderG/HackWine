from typing import List

from fastapi import APIRouter, Depends
from database.base import AsyncDatabase
from database.repositories.UserRepository import UsersRepository
from database.models.users import UserLogin, UserRead, UserReg

router = APIRouter()


@router.post('/login', name='Auth', response_model=UserRead)
async def auth_user(login: UserLogin, session=Depends(AsyncDatabase.get_session)):
    return await UsersRepository(session).login(login)


@router.get('/all', name='get all user', response_model=List[UserRead])
async def all_user(session=Depends(AsyncDatabase.get_session)):
    return await UsersRepository(session).all()


@router.get('/{user_id}', name='get user by id', response_model=UserRead)
async def user_by_id(user_id: int, session=Depends(AsyncDatabase.get_session)):
    return await UsersRepository(session).by_id(user_id)


@router.post('/registration', name='user registration', response_model=UserRead)
async def registration_user(RegData: UserReg, session=Depends(AsyncDatabase.get_session)):
    return await UsersRepository(session).registration(RegData)


@router.delete('/{user_id}', name='delete user by id')
async def del_user(user_id: int, session=Depends(AsyncDatabase.get_session)):
    return await UsersRepository(session).delete(user_id)
