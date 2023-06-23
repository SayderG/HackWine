from typing import List

from fastapi import APIRouter, Depends
from database.base import AsyncDatabase
from database.repositories.CardRepository import CardRepository
from database.models.cards import CardCreate, CardRead

router = APIRouter()


@router.post('/', name='create card')
async def create_card(card: CardCreate, session=Depends(AsyncDatabase.get_session)):
    return await CardRepository(session).create(card.__dict__)


@router.get('/all', name='get all cards', response_model=List[CardRead])
async def all_cards(session=Depends(AsyncDatabase.get_session)):
    return await CardRepository(session).all()


@router.get('/{card_id}', name='get card by id', response_model=CardRead)
async def card_by_id(card_id: int, session=Depends(AsyncDatabase.get_session)):
    return await CardRepository(session).by_id(card_id)


@router.delete('/{card_id}', name='delete card by id')
async def del_card(card_id: int, session=Depends(AsyncDatabase.get_session)):
    return await CardRepository(session).delete(card_id)
