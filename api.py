from fastapi import FastAPI, APIRouter
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from API.routers import root, users, chat, cards, kanban, points, cells
from API.redis import stop_redis, start_redis, redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

app = FastAPI(secure=False)
main_router = APIRouter()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

main_router.include_router(root.router, tags=['root'])
main_router.include_router(users.router, tags=['users'], prefix='/users')
main_router.include_router(cards.router, tags=['cards'], prefix='/cards')
main_router.include_router(kanban.router, tags=['kanban'], prefix='/kanban')
main_router.include_router(points.router, tags=['points'], prefix='/points')
main_router.include_router(cells.router, tags=['cells'], prefix='/cells')
main_router.include_router(chat.router, tags=['chats'], prefix='/chats')

app.include_router(main_router, prefix='/api/v1')


@app.on_event("startup")
async def startup_event():
    await start_redis()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.on_event("shutdown")
async def shutdown_event():
    await stop_redis()


if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=8008, reload=True)
