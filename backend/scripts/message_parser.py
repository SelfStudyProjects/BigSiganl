"""
텔레그램 메시지 파싱기
"""
IMPORT re, datetime
FROM trades.models IMPORT Trade

CLASS BigSignalParser:
    METHOD parse_message(message_text, message_datetime):
        # HOLD 시그널 체크 (거래하지 않음)
        hold_pattern = r'^([A-Z]+)\\s*\\n.*시그널:\\s*HOLD'
        IF re.search(hold_pattern, message_text):
            RETURN None  # HOLD는 실제 거래가 아니므로 저장하지 않음
        
        # BUY/SELL 시그널 파싱
        trade_pattern = r'^(Buy|Sell)\\s+([A-Z]+)\\s+📈|📉'
        trade_match = re.search(trade_pattern, message_text)
        
        IF NOT trade_match:
            RETURN None
        
        action = trade_match.group(1).upper()  # BUY 또는 SELL
        asset = trade_match.group(2).upper()   # BTC, DOGE 등
        
        # 현재 가격 추출
        price_pattern = r'현재 가격\\s*:\\s*([\\d,]+)\\s*KRW'
        price_match = re.search(price_pattern, message_text)
        IF NOT price_match:
            RETURN None
        
        price = CONVERT price_match.group(1) to float (remove commas)
        
        # 매수/매도 비율 추출
        IF action == 'BUY':
            ratio_pattern = r'매수 비율\\s*:\\s*([\\d.]+)%'
        ELSE:
            ratio_pattern = r'매도 비율\\s*:\\s*([\\d.]+)%'
        
        ratio_match = re.search(ratio_pattern, message_text)
        IF NOT ratio_match:
            RETURN None
        
        percentage = CONVERT ratio_match.group(1) to float
        
        RETURN {
            'timestamp': message_datetime,
            'asset': asset,
            'action': action,
            'price': price,
            'percentage': percentage,
            'base_currency': 'KRW',
            'raw_message': message_text
        }
    
    METHOD save_trade_to_db(trade_data):
        TRY:
            CREATE Trade instance with trade_data
            SAVE to database
            RETURN True
        EXCEPT Exception as e:
            LOG error message
            RETURN False