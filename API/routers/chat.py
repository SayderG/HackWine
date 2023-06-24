from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
from fastapi import APIRouter
from API.redis import redis

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        pass

    async def connect(self, websocket: WebSocket, group: str, username: str):
        await websocket.accept()
        connection_key = f"{group}:{username}"
        await redis.sadd("active_connections", connection_key)
        await redis.sadd(f"connections:{group}", connection_key)

    async def disconnect(self, websocket: WebSocket, group: str, username: str):
        connection_key = f"{group}:{username}"
        await redis.srem("active_connections", connection_key)
        await redis.srem(f"connections:{group}", connection_key)

    async def send_personal_message(self, message: str, group: str, username: str):
        connection_key = f"{group}:{username}"
        connections = await redis.smembers(connection_key)
        for connection in connections:
            websocket = WebSocket(connection)
            await websocket.send_text(message)

    async def broadcast(self, message: str, group: str, add_to_db: bool):
        if add_to_db:
            await self.add_message_to_database(message, group)
        connections = await redis.smembers(f"connections:{group}")
        for connection in connections:
            websocket = WebSocket(connection)
            await websocket.send_text(message)

    async def add_message_to_database(self, message: str, group: str):
        await redis.rpush(f"messages:{group}", message)

    async def get_messages_from_database(self, group: str):
        messages = await redis.lrange(f"messages:{group}", 0, -1)
        return [message.decode() for message in messages]


manager = ConnectionManager()

@router.websocket("/ws/{group}/{username}")
async def websocket_endpoint(websocket: WebSocket, group: str, username: str):
    await manager.connect(websocket, group, username)

    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(message, group, add_to_db=True)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, group, username)


@router.get("/messages/{group}")
async def get_messages(group: str):
    messages = await manager.get_messages_from_database(group)
    return {"messages": messages}
