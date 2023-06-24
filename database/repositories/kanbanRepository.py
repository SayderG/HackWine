from fastapi import HTTPException
from sqlalchemy import select
from database.models.columns import Columns, ColumnCreate
from database.models.cards import Cards, CardCreate
from database.repositories.BaseRepository import BaseRepository


class KanbanRepository(BaseRepository):
    model = Columns

    async def all(self):
        query = await self.session.execute(select(Columns).order_by(Columns.id))
        columns = query.scalars().all()
        for column in columns:
            column.count = len(column.cards)
        await self.session.commit()
        return columns

    # funnels
    async def create_column(self, data: ColumnCreate):
        column = Columns(**data.__dict__)
        self.session.add(column)
        await self.session.commit()
        return column

    async def update_column(self, column_id: int, data: dict):
        column = await self.session.get(Columns, column_id)
        column.title = data['title']
        await self.session.commit()
        return column

    # cards
    async def move_card(self, card_id: int, column_id: int):
        card = await self.session.get(Cards, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="card not found")
        card.column_id = column_id
        await self.session.commit()
        return card
