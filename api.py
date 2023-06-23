import aioredis as aioredis
from fastapi import FastAPI, APIRouter
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from API.routers import root, users, chat, cards, kanban

app = FastAPI()
main_router = APIRouter()
redis = None

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "PATCH", "HEAD"],
    allow_headers=["*"],
    max_age=3600,
)

main_router.include_router(root.router, tags=['root'])
main_router.include_router(users.router, tags=['users'], prefix='/users')
main_router.include_router(cards.router, tags=['cards'], prefix='/cards')
main_router.include_router(kanban.router, tags=['kanban'], prefix='/kanban')
main_router.include_router(chat.router, tags=['chats'], prefix='/chats')

app.include_router(main_router, prefix='/api/v1')


@app.on_event("startup")
async def startup_event():
    global redis
    redis = await aioredis.from_url("redis://localhost")


@app.on_event("shutdown")
async def shutdown_event():
    redis.close()
    await redis.wait_closed()


if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=8000, reload=True)
