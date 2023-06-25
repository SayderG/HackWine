from sqlalchemy import select

from database.repositories.BaseRepository import BaseRepository
from database.models.cellsPredict import Cell_predicts


class CellPredictRepository(BaseRepository):
    model = Cell_predicts

    async def by_cell_id(self, cell_id: int):
        query = await self.session.execute(select(Cell_predicts).where(Cell_predicts.place == cell_id))
        return query.scalars().first()
