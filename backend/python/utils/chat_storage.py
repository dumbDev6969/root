import json
import os
from typing import List, Dict

CHAT_HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'chat_history.json')

def load_chat_history(user_uuid: str) -> List[Dict]:
    """
    Load chat history for the given user UUID from JSON file.
    """
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []
    with open(CHAT_HISTORY_FILE, 'r') as file:
        data = json.load(file)
    return data.get(user_uuid, [])

def save_chat_message(message: Dict):
    """
    Save a chat message to the JSON file.
    """
    if not os.path.exists(CHAT_HISTORY_FILE):
        data = {}
    else:
        with open(CHAT_HISTORY_FILE, 'r') as file:
            data = json.load(file)
    sender = message["sender_uuid"]
    receiver = message["receiver_uuid"]
    # Initialize sender and receiver chat histories if not present
    if sender not in data:
        data[sender] = []
    if receiver not in data:
        data[receiver] = []
    # Append message to both sender and receiver histories
    data[sender].append(message)
    data[receiver].append(message)
    with open(CHAT_HISTORY_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def search_chat_history(user_uuid: str, query: str) -> List[Dict]:
    """
    Search chat history for a given query.
    """
    chat_history = load_chat_history(user_uuid)
    filtered = [msg for msg in chat_history if query.lower() in msg["content"].lower()]
    return filtered