from database.repositories.BaseRepository import BaseRepository
from database.models.cells import Cells


class CellRepository(BaseRepository):
    model = Cells

