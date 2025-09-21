#!/usr/bin/env python
"""
BigSignal 채널 메시지 간단 테스트
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

async def test_channel_messages():
    """
    채널의 최근 메시지들을 간단히 조회
    """
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    channel_id = int(os.getenv('TELEGRAM_CHANNEL_ID', 0))
    
    client = TelegramClient('test_session', api_id, api_hash)
    
    try:
        await client.start(phone=phone)
        
        # 채널 찾기
        channel = None
        async for dialog in client.iter_dialogs():
            if 'bigsignal' in dialog.name.lower() or 'big' in dialog.name.lower():
                channel = dialog.entity
                print(f"채널 발견: {dialog.name}")
                break
        
        if not channel:
            print("BigSignal 채널을 찾을 수 없습니다")
            return
        
        print(f"채널 ID: {channel.id}")
        print(f"채널 타입: {type(channel).__name__}")
        
        # 최근 메시지 10개 조회
        print("\n=== 최근 메시지 10개 ===")
        count = 0
        async for message in client.iter_messages(channel, limit=10):
            count += 1
            if message.message:
                preview = message.message[:100].replace('\n', ' ')
                print(f"{count}. {message.date} - {preview}...")
            else:
                print(f"{count}. {message.date} - [미디어/빈 메시지]")
        
        print(f"\n총 {count}개 메시지 조회됨")
        
        # 전체 메시지 개수 확인
        print("\n=== 전체 메시지 개수 확인 ===")
        total = 0
        async for message in client.iter_messages(channel, limit=100):
            total += 1
        
        print(f"최근 100개 중 실제 메시지: {total}개")
        
    except Exception as e:
        print(f"오류 발생: {e}")
    
    finally:
        await client.disconnect()

if __name__ == "__main__":
    print("=== BigSignal 채널 메시지 테스트 ===")
    asyncio.run(test_channel_messages())