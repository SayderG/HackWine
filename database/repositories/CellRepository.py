from database.repositories.BaseRepository import BaseRepository
from database.models.cells import Cells
from ML.app_predictions import get_prediction

class CellRepository(BaseRepository):
    model = Cells

    async def predict(self, cell_id: int):
        cell = await self.by_id(cell_id)
        predict = get_prediction(cell)
        return predict
