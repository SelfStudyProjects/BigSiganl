#!/usr/bin/env python
"""
텔레그램 채널 ID 찾기 도구
"""

import os
import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

async def find_channels():
    """
    사용자가 가입한 모든 채널/그룹 목록 출력
    """
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    
    client = TelegramClient('channel_finder', api_id, api_hash)
    
    try:
        await client.start(phone=phone)
        
        print("=== 가입한 채널/그룹 목록 ===")
        print()
        
        # 모든 대화(채널/그룹) 가져오기
        async for dialog in client.iter_dialogs():
            if dialog.is_channel or dialog.is_group:
                channel_type = "채널" if dialog.is_channel else "그룹"
                print(f"📢 {dialog.name}")
                print(f"   타입: {channel_type}")
                print(f"   ID: {dialog.id}")
                print(f"   Username: @{dialog.username}" if dialog.username else "   Username: 없음")
                print()
                
                # BigSignal 관련 키워드 확인
                if any(keyword in dialog.name.lower() for keyword in ['big', 'signal', 'bigsignal']):
                    print(f"🎯 BigSignal 관련 채널 발견!")
                    print(f"   사용할 ID: {dialog.id}")
                    print()
        
        print("=== 검색 완료 ===")
        print("BigSignal 채널을 찾으면 해당 ID를 .env 파일에 입력하세요")
        
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(find_channels())