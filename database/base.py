import sqlalchemy.engine.url as SQURL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlmodel import SQLModel
from database.settings import Settings
from database.models.users import Users

Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        db = Settings()
        URL = SQURL.URL.create(
            drivername="postgresql+asyncpg",
            username=db.user,
            password=db.password,
            host=db.host,
            port=db.port,
            database=db.database
        )
        self._engine = create_async_engine(URL, echo=True)
        self._session = sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False)

    async def create_db(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def get_session_maker(self) -> sessionmaker:
        return self._session

    async def get_session(self) -> AsyncSession:
        async with self._session() as session:
            yield session


AsyncDatabase = AsyncDatabaseSession()
