from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
import os
from uuid import UUID
from utils.logger import logger

chat_router = APIRouter()

CHAT_HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'chat_history.json')

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_uuid: str, websocket: WebSocket):
        try:
            # Check if an existing connection exists for this user
            if user_uuid in self.active_connections:
                logger.info(f"User {user_uuid} is already connected. Skipping reconnection.")
                return True

            await websocket.accept()
            self.active_connections[user_uuid] = websocket
            logger.info(f"User {user_uuid} connected successfully")
            return True
        except Exception as e:
            logger.info(f"Error connecting user {user_uuid}: {str(e)}")
            try:
                await websocket.close(code=1011)
            except:
                pass
            return False

    def disconnect(self, user_uuid: str):
        if user_uuid in self.active_connections:
            try:
                del self.active_connections[user_uuid]
                logger.info(f"User {user_uuid} disconnected cleanly")
            except Exception as e:
                logger.info(f"Error disconnecting user {user_uuid}: {str(e)}")

    async def send_personal_message(self, message: Dict, user_uuid: str):
        websocket = self.active_connections.get(user_uuid)
        if websocket:
            try:
                await websocket.send_json(message)
                logger.info(f"Sent message to {user_uuid}: {message}")
                return True
            except Exception as e:
                logger.info(f"Error sending message to {user_uuid}: {str(e)}")
                # Remove dead connection
                self.disconnect(user_uuid)
                return False
        return False

    async def broadcast(self, message: Dict):
        disconnected_users = []
        for user_uuid, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
                logger.info(f"Broadcasted message to {user_uuid}: {message}")
            except Exception as e:
                logger.info(f"Error broadcasting to {user_uuid}: {str(e)}")
                disconnected_users.append(user_uuid)
        
        # Clean up dead connections
        for user_uuid in disconnected_users:
            self.disconnect(user_uuid)

manager = ConnectionManager()

async def get_user_uuid(websocket: WebSocket):
    user_uuid = websocket.query_params.get("uuid")
    if not user_uuid:
        await websocket.close(code=1008)
        raise HTTPException(status_code=400, detail="UUID not provided")
    
    # Handle custom UUID formats (USR and EMP_ prefixes)
    if user_uuid.startswith('USR') or user_uuid.startswith('EMP_'):
        return user_uuid
        
    try:
        # Try standard UUID validation if no prefix
        UUID(user_uuid, version=4)
        return user_uuid
    except ValueError:
        logger.info(f"Invalid UUID format received: {user_uuid}")
        await websocket.close(code=1008)
        raise HTTPException(status_code=400, detail="Invalid UUID format")

@chat_router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, user_uuid: str = Depends(get_user_uuid)):
    try:
        connected = await manager.connect(user_uuid, websocket)
        if not connected:
            logger.info(f"Failed to establish WebSocket connection for user {user_uuid}")
            try:
                await websocket.send_json({
                    "type": "error",
                    "message": "Failed to establish connection",
                    "details": "Server connection error"
                })
            except:
                pass
            return
        
        logger.info(f"WebSocket connection established for user {user_uuid}")
        online_message = {"type": "status", "user_uuid": user_uuid, "status": "online"}
        await manager.broadcast(online_message)

        # Send the list of currently online users to the newly connected user
        online_users = [{"user_uuid": uuid, "status": "online"} for uuid in manager.active_connections.keys()]
        await websocket.send_json({"type": "online_users", "users": online_users})
        logger.info(f"Online users sent to {user_uuid}: {online_users}")

        # Don't send chat history on initial connection
        # History will be requested per conversation
        logger.info(f"Connection setup complete for {user_uuid}")

        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "history_request":
                target_uuid = data.get("data", {}).get("target_uuid")
                if not target_uuid:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Target UUID not provided for history request"
                    })
                    continue

                chat_history = load_chat_history(user_uuid)
                # Filter history for conversations between these two users
                filtered_history = [
                    msg for msg in chat_history 
                    if (msg["sender_uuid"] == user_uuid and msg["receiver_uuid"] == target_uuid) or 
                       (msg["sender_uuid"] == target_uuid and msg["receiver_uuid"] == user_uuid)
                ]
                await websocket.send_json({
                    "type": "history",
                    "messages": filtered_history
                })
                print(f"Sent filtered chat history for {user_uuid} with {target_uuid}")
                continue

            elif message_type == "message":
                sender_uuid = data.get("sender_uuid")
                message_data = data.get("data", {})
                
                receiver_uuid = message_data.get("receiver_uuid")
                content = message_data.get("msg")
                timestamp = message_data.get("date")
                attachments = message_data.get("attachments", {
                    "images": [],
                    "videos": [],
                    "voice_message": []
                })

                if not receiver_uuid or not content or not timestamp:
                    await websocket.send_json({"type": "error", "message": "Invalid message format."})
                    continue

                try:
                    message = {
                        "sender_uuid": sender_uuid or user_uuid,
                        "receiver_uuid": receiver_uuid,
                        "content": content,
                        "timestamp": timestamp,
                        "attachments": attachments
                    }
                    # Always save the message first, regardless of recipient's online status
                    save_chat_message(message)
                    logger.info(f"Received message from {user_uuid} to {receiver_uuid}: {content}")

                    # Attempt to send message to receiver if they're online
                    sent = await manager.send_personal_message({"type": "message", "message": message}, receiver_uuid)
                    if not sent:
                        # Message is already saved, just notify sender that recipient is offline
                        await websocket.send_json({
                            "type": "response",
                            "status": "success",
                            "message": "Message saved. Recipient is offline and will receive it when they connect.",
                            "data": {
                                "timestamp": timestamp,
                                "receiver_uuid": receiver_uuid,
                                "delivery_status": "pending"
                            }
                        })
                        continue

                    logger.info(f"Message sent from {user_uuid} to {receiver_uuid}: {message}")

                    # Send success response to sender
                    await websocket.send_json({
                        "type": "response",
                        "status": "success",
                        "message": "Message sent successfully",
                        "data": {
                            "timestamp": timestamp,
                            "receiver_uuid": receiver_uuid
                        }
                    })
                except Exception as e:
                    logger.info(f"Error sending message: {str(e)}")
                    # Send error response to sender
                    await websocket.send_json({
                        "type": "response",
                        "status": "error",
                        "message": f"Failed to send message: {str(e)}",
                        "data": {
                            "timestamp": timestamp,
                            "receiver_uuid": receiver_uuid
                        }
                    })

            elif message_type == "search":
                query = data.get("query", "")
                search_results = search_chat_history(user_uuid, query)
                await websocket.send_json({"type": "search_results", "results": search_results})
                logger.info(f"Search results sent to {user_uuid}: {search_results}")
                logger.info(f"User {user_uuid} searched for: {query}")

            else:
                await websocket.send_json({"type": "error", "message": "Unknown message type."})
                logger.info(f"Unknown message type received: {message_type}")
    except WebSocketDisconnect:
        manager.disconnect(user_uuid)
        offline_message = {"type": "status", "user_uuid": user_uuid, "status": "offline"}
        logger.info(f"User {user_uuid} disconnected: WebSocket connection closed")
        try:
            await manager.broadcast(offline_message)
        except Exception as e:
            logger.info(f"Error broadcasting offline status: {str(e)}")
    except json.JSONDecodeError as e:
        logger.info(f"JSON decode error for user {user_uuid}: {str(e)}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": "Invalid message format: Please send valid JSON",
                "details": str(e)
            })
        except:
            pass
        finally:
            manager.disconnect(user_uuid)
    except Exception as e:
        logger.info(f"Unexpected error for user {user_uuid}: {str(e)}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": "Server error occurred",
                "details": str(e)
            })
        except:
            pass
        finally:
            manager.disconnect(user_uuid)
            try:
                await websocket.close(code=1001)
            except:
                pass

class ChatHistoryManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_data(self, data):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                chat_history = json.load(f)
        else:
            chat_history = []

        chat_history.append(data)

        with open(self.file_path, "w") as f:
            json.dump(chat_history, f)

    def read_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return []

    def get_sent_data(self, uuid):
        chat_history = self.read_data()
        return [message for message in chat_history if message['sender_uuid'] == uuid]

    def get_received_data(self, uuid):
        chat_history = self.read_data()
        return [message for message in chat_history if message['receiver_uuid'] == uuid]

chat_manager = ChatHistoryManager(CHAT_HISTORY_FILE)

def load_chat_history(user_uuid: str) -> List[Dict]:
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []
    with open(CHAT_HISTORY_FILE, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}
    user_history = data.get(user_uuid, [])
    logger.info(f"Loaded chat history for {user_uuid}: {user_history}")
    return user_history

def save_chat_message(message: Dict):
    if not os.path.exists(CHAT_HISTORY_FILE):
        data = {}
    else:
        with open(CHAT_HISTORY_FILE, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    
    # Ensure the message has all required fields
    processed_message = {
        "sender_uuid": message["sender_uuid"],
        "receiver_uuid": message["receiver_uuid"],
        "content": message.get("content", message.get("msg", "")),  # Support both old and new format
        "timestamp": message.get("timestamp", message.get("date", "")),  # Support both old and new format
        "attachments": message.get("attachments", {
            "images": [],
            "videos": [],
            "voice_message": []
        })
    }
    
    sender = processed_message["sender_uuid"]
    receiver = processed_message["receiver_uuid"]
    
    # Store messages for both sender and receiver
    data.setdefault(sender, []).append(processed_message)
    data.setdefault(receiver, []).append(processed_message)
    
    with open(CHAT_HISTORY_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    logger.info(f"Saved message for {sender} and {receiver}: {processed_message}")

def search_chat_history(user_uuid: str, query: str) -> List[Dict]:
    sent_messages = chat_manager.get_sent_data(user_uuid)
    received_messages = chat_manager.get_received_data(user_uuid)
    chat_history = sent_messages + received_messages
    filtered = [msg for msg in chat_history if query.lower() in msg["content"].lower()]
    logger.info(f"Search results for user {user_uuid} and query '{query}': {filtered}")
    return filtered
