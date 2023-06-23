from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
from fastapi import APIRouter
from API.redis import redis

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/group/user");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)


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
