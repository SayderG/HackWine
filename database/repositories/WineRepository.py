import datetime

from fastapi import HTTPException

from database.repositories.BaseRepository import BaseRepository
from database.models.Wine import Wines
from database.models.wineStages import Wine_stages, WineStageCreate


class WineRepository(BaseRepository):
    model = Wines

    async def change_stage(self, wine_id):
        wine = await self.by_id(wine_id)
        if not wine:
            raise HTTPException(status_code=404, detail="Wine not found")
        stages: list = wine.stages
        last_stage = [stage for stage in stages if stage.last][0]
        last_stage_index = stages.index(last_stage)
        print(last_stage_index)
        last_stage.last = False
        last_stage.changed_at = datetime.datetime.now()
        next_stage = stages[last_stage_index + 1]
        next_stage.last = True
        next_stage.started_at = datetime.datetime.now()

        await self.session.commit()
        return next_stage

    async def create_stage(self, wine_id, data: WineStageCreate):
        wine = await self.by_id(wine_id)
        if not wine:
            raise HTTPException(status_code=404, detail="Wine not found")
        stage = Wine_stages(**data.__dict__, wine_id=wine_id)
        stages = wine.stages
        if len(stages) == 0:
            stage.last = True
            stage.started_at = datetime.datetime.now()
        wine.stages.append(stage)
        await self.session.commit()
        return stage
