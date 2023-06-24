from typing import List
from fastapi import APIRouter, Depends
from database.base import AsyncDatabase
from database.repositories.CellRepository import CellRepository
from database.models.cells import CellRead, CellCreate
from fastapi_cache.decorator import cache

router = APIRouter()


@router.post('/', name='create cell')
async def create_cell(cell: CellCreate, session=Depends(AsyncDatabase.get_session)):
    return await CellRepository(session).create(cell.__dict__)


@router.get('/all', name='get all cells', response_model=List[CellRead])
@cache(expire=60)
async def all_cells(session=Depends(AsyncDatabase.get_session)):
    return await CellRepository(session).all()


@router.get('/{cell_id}', name='get cell by id', response_model=CellRead)
@cache(expire=120)
async def cell_by_id(cell_id: int, session=Depends(AsyncDatabase.get_session)):
    return await CellRepository(session).by_id(cell_id)


@router.delete('/{sel_id}', name='delete cell by id')
async def del_cell(cell_id: int, session=Depends(AsyncDatabase.get_session)):
    return await CellRepository(session).delete(cell_id)
