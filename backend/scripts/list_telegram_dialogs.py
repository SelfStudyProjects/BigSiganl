"""
List Telegram dialogs and print id, username, and title to help pick the correct channel identifier.
Usage:
  python list_telegram_dialogs.py

It uses the same .env config as other scripts (TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE).
"""
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = os.getenv('TELEGRAM_PHONE')

async def main():
    client = TelegramClient('historical_session', API_ID, API_HASH)
    await client.start(phone=PHONE)
    print('Connected. Fetching dialogs...')
    count = 0
    async for dialog in client.iter_dialogs():
        ent = dialog.entity
        ent_id = getattr(ent, 'id', None)
        ent_username = getattr(ent, 'username', None)
        ent_title = getattr(ent, 'title', None) or getattr(ent, 'first_name', None) or dialog.name
        print(f'id={ent_id}\tusername={ent_username}\ttitle={ent_title}')
        count += 1
        if count >= 200:
            break
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
