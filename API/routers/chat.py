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
    <title>WebSocket Chat</title>
    <script type="text/javascript">
        var socket;

        function connectWebSocket(group, username) {
            var wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
            var wsUrl = wsProtocol + window.location.host + "/ws/" + group + "/" + username;

            socket = new WebSocket(wsUrl);

            socket.onopen = function () {
                console.log("WebSocket connection established.");
            };

            socket.onmessage = function (event) {
                var message = event.data;
                // Handle received message
                console.log("Received message:", message);
            };

            socket.onclose = function () {
                console.log("WebSocket connection closed.");
            };
        }

        function sendMessage(message) {
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(message);
            }
        }

        function connectToMessageStream(group) {
            var wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
            var wsUrl = wsProtocol + window.location.host + "/ws/" + group + "/stream";

            socket = new WebSocket(wsUrl);

            socket.onopen = function () {
                console.log("WebSocket connection established for message stream.");
            };

            socket.onmessage = function (event) {
                var message = event.data;
                // Handle received message from the message stream
                console.log("Received message from stream:", message);
            };

            socket.onclose = function () {
                console.log("WebSocket connection for message stream closed.");
            };
        }

        function disconnectWebSocket() {
            if (socket) {
                socket.close();
            }
        }
    </script>
</head>
<body>
    <h1>WebSocket Chat</h1>
    <div>
        <h2>Connect to WebSocket</h2>
        <form onsubmit="return false;">
            <label for="group">Group:</label>
            <input type="text" id="group" name="group">
            <br>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username">
            <br>
            <button onclick="connectWebSocket(document.getElementById('group').value, document.getElementById('username').value)">
                Connect
            </button>
        </form>
    </div>
    <div>
        <h2>Send Message</h2>
        <form onsubmit="return false;">
            <label for="message">Message:</label>
            <input type="text" id="message" name="message">
            <br>
            <button onclick="sendMessage(document.getElementById('message').value)">Send</button>
        </form>
    </div>
    <div>
        <h2>Message Stream</h2>
        <form onsubmit="return false;">
            <label for="streamGroup">Group:</label>
            <input type="text" id="streamGroup" name="streamGroup">
            <br>
            <button onclick="connectToMessageStream(document.getElementById('streamGroup').value)">
                Connect to Stream
            </button>
        </form>
    </div>
    <button onclick="disconnectWebSocket()">Disconnect</button>
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
