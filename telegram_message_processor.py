import os
import re
import csv
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
import asyncio
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramMessageProcessor:
    def __init__(self, api_id, api_hash, phone, channel_username):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.channel_username = channel_username
        self.client = None
        self.csv_file = 'trades.csv'
        self.csv_headers = ['timestamp', 'asset', 'action', 'price', 'percentage', 'base_currency']
        
    async def initialize(self):
        """텔레그램 클라이언트 초기화"""
        self.client = TelegramClient('session_name', self.api_id, self.api_hash)
        await self.client.start(phone=self.phone)
        
        # CSV 파일이 없으면 헤더 생성
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.csv_headers)
                writer.writeheader()
    
    def parse_message(self, message_text):
        """텔레그램 메시지를 파싱하여 거래 정보 추출"""
        try:
            # 기본 패턴 정의
            patterns = {
                'buy': r'Buy\s+(\w+).*?현재\s*가격\s*:\s*([\d,]+)\s*(\w+).*?매수\s*비율\s*:\s*([\d.]+)%',
                'sell': r'Sell\s+(\w+).*?현재\s*가격\s*:\s*([\d,]+)\s*(\w+).*?매도\s*비율\s*:\s*([\d.]+)%'
            }
            
            for action, pattern in patterns.items():
                match = re.search(pattern, message_text, re.IGNORECASE | re.DOTALL)
                if match:
                    asset, price, currency, percentage = match.groups()
                    return {
                        'timestamp': datetime.now().isoformat(),
                        'asset': asset.strip(),
                        'action': action,
                        'price': float(price.replace(',', '')),
                        'percentage': float(percentage),
                        'base_currency': currency.strip()
                    }
            return None
        except Exception as e:
            logger.error(f"메시지 파싱 중 오류 발생: {str(e)}")
            return None
    
    async def save_to_csv(self, trade_data):
        """거래 데이터를 CSV 파일에 저장"""
        try:
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.csv_headers)
                writer.writerow(trade_data)
            logger.info(f"거래 데이터 저장 완료: {trade_data}")
        except Exception as e:
            logger.error(f"CSV 저장 중 오류 발생: {str(e)}")
    
    async def message_handler(self, event):
        """텔레그램 메시지 핸들러"""
        try:
            trade_data = self.parse_message(event.message.text)
            if trade_data:
                await self.save_to_csv(trade_data)
        except Exception as e:
            logger.error(f"메시지 처리 중 오류 발생: {str(e)}")
    
    async def start_listening(self):
        """텔레그램 채널 메시지 수신 시작"""
        try:
            channel = await self.client.get_entity(self.channel_username)
            self.client.add_event_handler(
                self.message_handler,
                events.NewMessage(chats=channel)
            )
            logger.info(f"채널 {self.channel_username} 메시지 수신 시작")
            await self.client.run_until_disconnected()
        except Exception as e:
            logger.error(f"메시지 수신 중 오류 발생: {str(e)}")

async def main():
    # 환경 변수나 설정 파일에서 가져와야 할 값들
    api_id = "YOUR_API_ID"
    api_hash = "YOUR_API_HASH"
    phone = "YOUR_PHONE_NUMBER"
    channel_username = "YOUR_CHANNEL_USERNAME"
    
    processor = TelegramMessageProcessor(api_id, api_hash, phone, channel_username)
    await processor.initialize()
    await processor.start_listening()

if __name__ == "__main__":
    asyncio.run(main()) 