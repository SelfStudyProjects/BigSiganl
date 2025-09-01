import requests
import json
import os

TELEGRAM_API_URL = "https://api.telegram.org/bot{}/"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def collect_telegram_messages():
    url = TELEGRAM_API_URL.format(TOKEN) + "getUpdates"
    response = requests.get(url)
    
    if response.status_code == 200:
        updates = response.json().get("result", [])
        for update in updates:
            process_message(update)
    else:
        print("Failed to fetch messages:", response.status_code)

def process_message(update):
    message = update.get("message")
    if message:
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text")
        print(f"Received message from {chat_id}: {text}")
        # Here you can add logic to save the message or perform other actions

if __name__ == "__main__":
    collect_telegram_messages()