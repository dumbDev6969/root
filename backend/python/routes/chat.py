from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import os

chat_router = APIRouter()

# Dictionary to store connected WebSocket clients
connected_users: Dict[str, WebSocket] = {}

# File to store chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Ensure the chat history file exists
if not os.path.exists(CHAT_HISTORY_FILE):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump({}, f)

def save_chat(sender: str, recipient: str, message: str):
    """Save chat messages to a JSON file for both users."""
    try:
        with open(CHAT_HISTORY_FILE, "r") as f:
            chat_history = json.load(f)

        if sender not in chat_history:
            chat_history[sender] = []
        if recipient not in chat_history:
            chat_history[recipient] = []

        chat_entry = {"to": recipient, "message": message}
        chat_history[sender].append(chat_entry)

        chat_entry_reverse = {"to": sender, "message": message}
        chat_history[recipient].append(chat_entry_reverse)

        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump(chat_history, f, indent=4)
    except Exception as e:
        print(f"Error saving chat: {e}")

async def get_chat_history(user_id: str) -> List[dict]:
    """Get chat history for a specific user."""
    try:
        with open(CHAT_HISTORY_FILE, "r") as f:
            chat_history = json.load(f)
            return chat_history.get(user_id, [])
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error getting chat history: {e}")
        return []

async def broadcast_online_users():
    """Broadcast the list of online users to all connected clients."""
    online_users = list(connected_users.keys())
    for user_ws in connected_users.values():
        try:
            await user_ws.send_json({
                "type": "online_users",
                "users": online_users
            })
        except Exception as e:
            print(f"Error broadcasting users: {e}")

@chat_router.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: str, websocket: WebSocket):
    await websocket.accept()
    connected_users[user_id] = websocket

    try:
        # Send initial messages
        await websocket.send_json({"type": "system", "message": "Connected successfully"})
        await broadcast_online_users()
        
        history = await get_chat_history(user_id)
        await websocket.send_json({"type": "chat_history", "history": history})

        # Main message loop
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                recipient = msg.get("to")
                message = msg.get("message")

                if not recipient or not message:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Missing recipient or message"
                    })
                    continue

                # Save message
                save_chat(user_id, recipient, message)

                # Send to recipient if online
                if recipient in connected_users:
                    await connected_users[recipient].send_json({
                        "user": user_id,
                        "message": message
                    })
                    # Confirm to sender
                    await websocket.send_json({
                        "type": "sent",
                        "to": recipient,
                        "message": message
                    })
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"User {recipient} is not online"
                    })

            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid message format"
                })
            except Exception as e:
                print(f"Error processing message: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": "Error processing message"
                })

    except WebSocketDisconnect:
        print(f"Client disconnected: {user_id}")
    finally:
        if user_id in connected_users:
            del connected_users[user_id]
            await broadcast_online_users()