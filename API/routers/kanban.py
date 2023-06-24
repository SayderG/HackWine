from typing import List
from database.repositories.kanbanRepository import KanbanRepository
from fastapi import APIRouter, Depends, HTTPException
from database.base import AsyncDatabase
from database.models.columns import ColumnRead, ColumnCreate
from database.models.cards import CardRead, CardCreate

router = APIRouter()


@router.post("/", response_model=ColumnRead, name='crete column', status_code=201)
async def create_column(column: ColumnCreate, db=Depends(AsyncDatabase.get_session)):
    return await KanbanRepository(db).create(column.__dict__)


@router.get("/", name='get all columns', response_model=List[ColumnRead])
async def get_column(db=Depends(AsyncDatabase.get_session)):
    columns = await KanbanRepository(db).all()
    if not columns:
        raise HTTPException(status_code=404, detail="Column not found")
    return columns


@router.delete("/{column_id}", name='delete column')
async def delete_column(column_id: int, db=Depends(AsyncDatabase.get_session)):
    column = await KanbanRepository(db).by_id(column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    await KanbanRepository(db).delete(column_id)


@router.get("/{column_id}", name='get by id column', response_model=ColumnRead)
async def get_column(column_id: int, db=Depends(AsyncDatabase.get_session)):
    column = await KanbanRepository(db).by_id(column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return column


@router.put("/columns/{column_id}/cards/{card_id}", name='move card', response_model=CardRead)
async def move_card(column_id: int, task_id: int, db=Depends(AsyncDatabase.get_session)):
    column = await KanbanRepository(db).by_id(column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return await KanbanRepository(db).move_card(task_id, column_id)
