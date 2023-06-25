from sqlalchemy import select
from database.repositories.BaseRepository import BaseRepository
from database.models.cells import Cells
from database.models.cellsPredict import Cell_predicts
from ML.app_predictions import get_prediction


class CellRepository(BaseRepository):
    model = Cells

    async def predict(self, cell_id: int):
        query = await self.session.execute(select(Cell_predicts).where(Cell_predicts.place == cell_id))
        cell_data = query.scalars().first()
        predict = get_prediction([cell_data.dict()])
        return predict
