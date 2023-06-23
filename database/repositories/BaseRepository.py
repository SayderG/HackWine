from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session: AsyncSession = session

    async def all(self, limit: int = 0, skip: int = 0):
        query = select(self.model)
        if skip:
            query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def by_id(self, model_id: int):
        query = await self.session.execute(select(self.model).where(self.model.id == model_id))
        return query.scalars().first()

    async def create(self, data: dict):
        try:
            model = self.model(**data)
            self.session.add(model)
            await self.session.commit()
            return model
        except IntegrityError:
            return None

    async def delete(self, model_id: int):
        model = await self.by_id(model_id)
        if not model:
            return None
        await self.session.delete(model)
        await self.session.commit()
        return 200
