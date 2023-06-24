from fastapi import HTTPException

from database.repositories.BaseRepository import BaseRepository
from database.models.Wine import Wines, WineUpdate


class WineRepository(BaseRepository):
    model = Wines

    async def update(self, wine_id: int, wine_update: WineUpdate):
        wine = await self.by_id(wine_id)
        if not wine:
            return HTTPException(status_code=404, detail="Wine not found")
        [setattr(wine, k, v) for k, v in wine_update.dict().items() if v is not None]
        await self.session.commit()
        return wine
