from telethon.sync import TelegramClient
import re
import csv
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')
chat_id = int(os.getenv('CHAT_ID'))

client = TelegramClient('session_name', api_id, api_hash)

def parse_trade_message(message_text):
    """텔레그램 메시지를 파싱하여 거래 정보를 추출합니다."""
    try:
        action = 'SELL' if '📉 SELL' in message_text else 'BUY' if '📈 BUY' in message_text else None
        if not action:
            return None

        price_match = re.search(r'현재 가격\s*:\s*([\d,]+)\s*KRW', message_text)
        price = float(price_match.group(1).replace(',', '')) if price_match else None

        pair_match = re.search(r'거래 페어\s*:\s*(\w+-\w+)', message_text)
        pair = pair_match.group(1) if pair_match else None

        ratio_match = re.search(r'매[도수]\s*비율\s*:\s*([\d.]+)%', message_text)
        ratio = float(ratio_match.group(1)) if ratio_match else None

        if all([action, price, pair, ratio]):
            return {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'action': action,
                'pair': pair,
                'price': price,
                'ratio': ratio,
                'quote_currency': 'KRW'
            }
    except Exception as e:
        print(f"메시지 파싱 중 오류 발생: {e}")
    return None

async def main():
    await client.start(phone=phone)
    
    trades = []
    
    async for message in client.iter_messages(chat_id, offset_date=None, reverse=True):
        if message.text:
            trade_info = parse_trade_message(message.text)
            if trade_info:
                trades.append(trade_info)
                print(f"거래 정보 추출: {trade_info}")

    if trades:
        df = pd.DataFrame(trades)
        df.to_csv('trades.csv', index=False, encoding='utf-8-sig')
        print(f"총 {len(trades)}개의 거래 내역이 trades.csv 파일로 저장되었습니다.")

with client:
    client.loop.run_until_complete(main())