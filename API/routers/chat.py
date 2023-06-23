from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect
from fastapi import APIRouter
from API.redis import redis

router = APIRouter()


@router.websocket("/ws/{group}/{username}")
async def websocket_endpoint(websocket: WebSocket, group: str, username: str):
    await websocket.accept()

    channel_name = f"{group}:{username}"
    redis_pubsub = redis.pubsub()

    await redis_pubsub.subscribe(channel_name)

    try:
        while True:
            message = await websocket.receive_text()
            await redis.publish(channel_name, message)
    except WebSocketDisconnect:
        await redis_pubsub.unsubscribe(channel_name)
        await redis_pubsub.close()


@router.websocket("/ws/{group}/stream")
async def message_stream(websocket: WebSocket, group: str):
    await websocket.accept()

    channel_name = f"{group}:*"
    redis_pubsub = redis.pubsub()

    await redis_pubsub.psubscribe(channel_name)

    try:
        while True:
            message = await redis_pubsub.get_message()
            if message and message["type"] == "message":
                await websocket.send_text(message["data"].decode())
    except WebSocketDisconnect:
        await redis_pubsub.punsubscribe(channel_name)
        await redis_pubsub.close()
