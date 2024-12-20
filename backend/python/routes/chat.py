from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
import os
from uuid import UUID

chat_router = APIRouter()

# Path to store chat history
CHAT_HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'chat_history.json')

# In-memory storage for connected clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_uuid: str, websocket: WebSocket):
        
        await websocket.accept()
        self.active_connections[user_uuid] = websocket
        print(f"User {user_uuid} connected.")

    def disconnect(self, user_uuid: str):
        if user_uuid in self.active_connections:
            del self.active_connections[user_uuid]
            print(f"User {user_uuid} disconnected.")

    async def send_personal_message(self, message: Dict, user_uuid: str):
        websocket = self.active_connections.get(user_uuid)
        if websocket:
            await websocket.send_json(message)
            print(f"Sent message to {user_uuid}: {message}")

    async def broadcast(self, message: Dict):
        for user_uuid, connection in self.active_connections.items():
            await connection.send_json(message)
            print(f"Broadcasted message to {user_uuid}: {message}")

manager = ConnectionManager()

# Dependency to extract UUID from query parameters
async def get_user_uuid(websocket: WebSocket):
    user_uuid = websocket.query_params.get("uuid")
    if not user_uuid:
        await websocket.close(code=1008)
        raise HTTPException(status_code=400, detail="UUID not provided")
    # Validate UUID format
    try:
        UUID(user_uuid, version=4)
    except ValueError:
        await websocket.close(code=1008)
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    return user_uuid

@chat_router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, user_uuid: str = Depends(get_user_uuid)):
    """
    WebSocket endpoint for real-time chat.
    """
    await manager.connect(user_uuid, websocket)
    try:
        # Notify others that user is online
        online_message = {"type": "status", "user_uuid": user_uuid, "status": "online"}
        await manager.broadcast(online_message)

        # Send existing chat history to the connected user
        chat_history = load_chat_history(user_uuid)
        await websocket.send_json({"type": "history", "messages": chat_history})

        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "message":
                receiver_uuid = data.get("receiver_uuid")
                content = data.get("content")
                timestamp = data.get("timestamp")
                if not receiver_uuid or not content or not timestamp:
                    await websocket.send_json({"type": "error", "message": "Invalid message format."})
                    continue

                message = {
                    "sender_uuid": user_uuid,
                    "receiver_uuid": receiver_uuid,
                    "content": content,
                    "timestamp": timestamp
                }
                save_chat_message(message)
                print(f"Received message from {user_uuid} to {receiver_uuid}: {content}")

                # Send message to receiver if online
                await manager.send_personal_message({"type": "message", "message": message}, receiver_uuid)

            elif message_type == "search":
                query = data.get("query", "")
                search_results = search_chat_history(user_uuid, query)
                await websocket.send_json({"type": "search_results", "results": search_results})
                print(f"User {user_uuid} searched for: {query}")

            else:
                await websocket.send_json({"type": "error", "message": "Unknown message type."})
                print(f"Unknown message type received: {message_type}")
    except WebSocketDisconnect:
        manager.disconnect(user_uuid)
        # Notify others that user is offline
        offline_message = {"type": "status", "user_uuid": user_uuid, "status": "offline"}
        await manager.broadcast(offline_message)
    except json.JSONDecodeError:
        await websocket.send_json({"type": "error", "message": "Invalid JSON format."})
        print("JSON decode error.")
    except Exception as e:
        manager.disconnect(user_uuid)
        await websocket.close(code=1001)
        print(f"Unexpected error: {e}")

def load_chat_history(user_uuid: str) -> List[Dict]:
    """
    Load chat history for the given user UUID from JSON file.
    """
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []
    with open(CHAT_HISTORY_FILE, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}
    return data.get(user_uuid, [])

def save_chat_message(message: Dict):
    """
    Save a chat message to the JSON file.
    """
    if not os.path.exists(CHAT_HISTORY_FILE):
        data = {}
    else:
        with open(CHAT_HISTORY_FILE, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    sender = message["sender_uuid"]
    receiver = message["receiver_uuid"]
    # Initialize sender and receiver chat histories if not present
    data.setdefault(sender, []).append(message)
    data.setdefault(receiver, []).append(message)
    with open(CHAT_HISTORY_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Saved message: {message}")

def search_chat_history(user_uuid: str, query: str) -> List[Dict]:
    """
    Search chat history for a given query.
    """
    chat_history = load_chat_history(user_uuid)
    filtered = [msg for msg in chat_history if query.lower() in msg["content"].lower()]
    print(f"Search results for user {user_uuid} and query '{query}': {filtered}")
    return filtered