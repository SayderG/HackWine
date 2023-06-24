from typing import List

from fastapi import APIRouter, Depends
from database.base import AsyncDatabase
from database.repositories.PointRepository import PointRepository
from database.models.points import PointCreate, PointRead
from fastapi_cache.decorator import cache

router = APIRouter()


@router.post('/', name='create point')
async def create_card(point: PointCreate, session=Depends(AsyncDatabase.get_session)):
    return await PointRepository(session).create(point.__dict__)


@router.get('/all', name='get all points', response_model=List[PointRead])
@cache(expire=60)
async def all_cards(session=Depends(AsyncDatabase.get_session)):
    return await PointRepository(session).all()


@router.get('/{point_id}', name='get point by id', response_model=PointRead)
async def card_by_id(point_id: int, session=Depends(AsyncDatabase.get_session)):
    return await PointRepository(session).by_id(point_id)


@router.delete('/{point_id}', name='delete point by id')
async def del_card(point_id: int, session=Depends(AsyncDatabase.get_session)):
    return await PointRepository(session).delete(point_id)
