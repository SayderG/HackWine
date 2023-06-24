from typing import List
from fastapi import APIRouter, Depends
from database.base import AsyncDatabase
from database.repositories.cellPredictRepository import CellPredictRepository
from database.models.cellsPredict import CellPredictCreate, CellPredictRead
from fastapi_cache.decorator import cache

router = APIRouter()


@router.post('/', name='create cellPredict')
async def create_cell_predict(cellPredict: CellPredictCreate, session=Depends(AsyncDatabase.get_session)):
    return await CellPredictRepository(session).create(cellPredict.__dict__)


@router.get('/all', name='get all cellPredicts', response_model=List[CellPredictRead])
@cache(expire=60)
async def sell_predict_all(session=Depends(AsyncDatabase.get_session)):
    return await CellPredictRepository(session).all()


@router.get('/cell/{cell_id}', name='get cellPredict by cell id', response_model=CellPredictRead)
@cache(expire=60)
async def sell_predict_by_cell_id(cell_id: int, session=Depends(AsyncDatabase.get_session)):
    return await CellPredictRepository(session).by_cell_id(cell_id)


@router.get('/{cellPredict_id}', name='get cellPredict by id', response_model=CellPredictRead)
async def sell_predict_by_id(cellPredict_id: int, session=Depends(AsyncDatabase.get_session)):
    return await CellPredictRepository(session).by_id(cellPredict_id)


@router.delete('/{cellPredict_id}', name='delete cellPredict by id')
async def del_cell_predict(cellPredict_id: int, session=Depends(AsyncDatabase.get_session)):
    return await CellPredictRepository(session).delete(cellPredict_id)
