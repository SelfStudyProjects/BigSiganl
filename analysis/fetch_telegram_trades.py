from telethon.sync import TelegramClient
import re
import csv
from datetime import datetime
import pandas as pd

api_id = '여기에_본인_API_ID'
api_hash = '여기에_본인_API_HASH'
phone = '여기에_본인_전화번호'

client = TelegramClient('session_name', api_id, api_hash)

def parse_trade_message(message_text):
    """텔레그램 메시지를 파싱하여 거래 정보를 추출합니다."""
    try:
        # 기본 정보 추출
        action = 'SELL' if '📉 SELL' in message_text else 'BUY' if '📈 BUY' in message_text else None
        if not action:
            return None

        # 가격 추출
        price_match = re.search(r'현재 가격\s*:\s*([\d,]+)\s*KRW', message_text)
        price = float(price_match.group(1).replace(',', '')) if price_match else None

        # 거래 페어 추출
        pair_match = re.search(r'거래 페어\s*:\s*(\w+-\w+)', message_text)
        pair = pair_match.group(1) if pair_match else None

        # 매도/매수 비율 추출
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
    chat_id = -1001234567890  # 예시: 실제 채널/그룹 ID로 변경
    
    # 거래 내역을 저장할 리스트
    trades = []
    
    async for message in client.iter_messages(chat_id, offset_date=None, reverse=True):
        if message.text:
            trade_info = parse_trade_message(message.text)
            if trade_info:
                trades.append(trade_info)
                print(f"거래 정보 추출: {trade_info}")

    # CSV 파일로 저장
    if trades:
        df = pd.DataFrame(trades)
        df.to_csv('trades.csv', index=False, encoding='utf-8-sig')
        print(f"총 {len(trades)}개의 거래 내역이 trades.csv 파일로 저장되었습니다.")

with client:
    client.loop.run_until_complete(main())
