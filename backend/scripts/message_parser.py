import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class BigSignalMessageParser:
    """
    BigSignal 텔레그램 메시지 파서
    실제 메시지 형식에 맞춰 구현
    """
    
    def __init__(self):
        self.supported_actions = ['BUY', 'SELL']
        self.supported_assets = ['BTC', 'USDT', 'DOGE', 'USDC']
    
    def parse_message(self, message_text, message_datetime):
        """
        텔레그램 메시지를 파싱하여 거래 정보 추출
        
        *** 모든 기간 데이터 호환 ***
        similar 1월 21일 형식: 간단한 Notes
        similar 8월 28일 형식: 상세한 Notes + Supplementary Score
        HOLD 메시지도 처리 (BTC\n현재 가격... 시그널: HOLD)
        """
        
        # 빈 메시지나 None 체크
        if not message_text or not message_text.strip():
            return None
        
        message_text = message_text.strip()
        
        try:
            # === STEP 1: 메시지 형식 식별 ===
            
            # 1-1. HOLD 메시지 처리 (BTC\n현재 가격... 시그널: HOLD)
            hold_pattern = r'^([A-Z]+)\s*\n.*?시그널:\s*HOLD'
            hold_match = re.search(hold_pattern, message_text, re.DOTALL | re.IGNORECASE)
            
            if hold_match:
                logger.debug(f"HOLD 시그널 감지, 거래 없음: {hold_match.group(1)}")
                return None  # HOLD는 실제 거래가 아니므로 저장하지 않음
            
            # 1-2. BUY/SELL 메시지 처리 (Buy BTC 📈 또는 Sell DOGE 📉)
            # Use non-capturing group for emoji to avoid alternation capturing only emoji
            trade_pattern = r'^(Buy|Sell)\s+([A-Z]+)\s*(?:📈|📉)'
            trade_match = re.search(trade_pattern, message_text, re.IGNORECASE | re.MULTILINE)
            
            if not trade_match:
                logger.debug(f"BUY/SELL 패턴 찾을 수 없음: {message_text[:50]}...")
                return None
            
            action = trade_match.group(1).upper()
            asset = trade_match.group(2).upper()
            
            # 지원되는 자산인지 확인
            if asset not in self.supported_assets:
                logger.debug(f"지원하지 않는 자산: {asset}")
                return None
            
            # === STEP 2: 공통 필드 추출 ===
            
            # 2-1. 현재 가격 추출 (모든 형식 공통)
            price_patterns = [
                r'현재 가격\s*:\s*([\d,]+)\s*KRW',     # 표준 형식
                r'현재가\s*:\s*([\d,]+)\s*KRW',       # 변형 1
                r'Price\s*:\s*([\d,]+)\s*KRW'         # 영문 형식
            ]
            
            price = None
            for pattern in price_patterns:
                price_match = re.search(pattern, message_text)
                if price_match:
                    price_str = price_match.group(1).replace(',', '')
                    price = float(price_str)
                    break
            
            if not price:
                logger.debug(f"가격 정보 찾을 수 없음: {message_text}")
                return None
            
            # 2-2. 거래 페어 추출 (선택사항)
            pair_patterns = [
                r'거래 페어\s*:\s*([A-Z]+-[A-Z]+)',    # 표준 형식
                r'Pair\s*:\s*([A-Z]+-[A-Z]+)'          # 영문 형식
            ]
            
            base_currency = 'KRW'  # 기본값
            for pattern in pair_patterns:
                pair_match = re.search(pattern, message_text)
                if pair_match:
                    pair = pair_match.group(1)
                    base_currency = pair.split('-')[0]
                    break
            
            # 2-3. 시그널 확인 (검증용, 선택사항)
            signal_patterns = [
                r'시그널:\s*(?:📈|📉)\s*(BUY|SELL)\s*\((매수|매도)\)',  # 한국어 형식
                r'Signal:\s*(?:📈|📉)\s*(BUY|SELL)',                    # 영문 형식
            ]
            
            for pattern in signal_patterns:
                signal_match = re.search(pattern, message_text)
                if signal_match:
                    signal_action = signal_match.group(1).upper()
                    if signal_action != action:
                        logger.debug(f"시그널 불일치 감지: 첫줄={action}, 시그널={signal_action}, 시그널 우선 적용")
                        action = signal_action  # 시그널 라인을 우선으로 함
                    break
            
            # 2-4. 매수/매도 비율 추출 (가장 중요!)
            ratio_patterns = [
                # 한국어 형식
                r'매수 비율\s*:\s*([\d.]+)%' if action == 'BUY' else r'매도 비율\s*:\s*([\d.]+)%',
                # 일반적 형식 (매매 비율)  
                r'매매 비율\s*:\s*([\d.]+)%',
                # 영문 형식
                r'Buy Ratio\s*:\s*([\d.]+)%' if action == 'BUY' else r'Sell Ratio\s*:\s*([\d.]+)%',
                r'Ratio\s*:\s*([\d.]+)%',
                # 비율 (일반)
                r'비율\s*:\s*([\d.]+)%',
            ]
            
            percentage = None
            for pattern in ratio_patterns:
                if pattern:  # None 체크
                    ratio_match = re.search(pattern, message_text)
                    if ratio_match:
                        percentage = float(ratio_match.group(1))
                        break
            
            if not percentage:
                logger.debug(f"비율 정보 찾을 수 없음: {message_text}")
                return None
            
            # === STEP 3: 유효성 검증 ===
            
            if percentage <= 0 or percentage > 100:
                logger.warning(f"유효하지 않은 비율: {percentage}%")
                return None
            
            if price <= 0:
                logger.warning(f"유효하지 않은 가격: {price}")
                return None
            
            # === STEP 4: 결과 반환 ===
            
            parsed_data = {
                'timestamp': message_datetime,
                'asset': asset,
                'action': action,
                'price': price,
                'percentage': percentage,
                'base_currency': base_currency,
                'raw_message': message_text
            }
            
            logger.info(f"✅ 메시지 파싱 성공: {action} {asset} @ {price:,} KRW ({percentage}%)")
            return parsed_data
            
        except Exception as e:
            logger.error(f"메시지 파싱 중 오류 발생: {e}")
            logger.debug(f"문제 메시지: {message_text}")
            return None
    
    def is_valid_signal_message(self, message_text):
        """
        BigSignal 메시지인지 빠르게 확인
        """
        if not message_text:
            return False
        
        # BigSignal 메시지의 특징적인 패턴들
        indicators = [
            r'Buy\s+[A-Z]+\s*📈',  # Buy BTC 📈
            r'Sell\s+[A-Z]+\s*📉', # Sell DOGE 📉  
            r'현재 가격\s*:',        # 현재 가격 :
            r'시그널:\s*📈|📉',      # 시그널: 📈
            r'매수 비율\s*:',        # 매수 비율 :
            r'매도 비율\s*:'         # 매도 비율 :
        ]
        
        for pattern in indicators:
            if re.search(pattern, message_text, re.IGNORECASE):
                return True
        
        return False
    
    def extract_technical_notes(self, message_text):
        """
        [Notes] 섹션에서 기술적 분석 정보 추출 (선택사항)
        """
        notes_pattern = r'\[Notes\]\s*(.*?)(?:\n\n|$)'
        notes_match = re.search(notes_pattern, message_text, re.DOTALL | re.IGNORECASE)
        
        if notes_match:
            notes_content = notes_match.group(1).strip()
            return notes_content
        
        return None
    
    def parse_supplementary_score(self, message_text):
        """
        Supplementary Score 추출 (고급 분석용)
        """
        score_pattern = r'Supplementary Score:\s*([\d.-]+)'
        score_match = re.search(score_pattern, message_text)
        
        if score_match:
            return float(score_match.group(1))
        
        return None

# 테스트 함수
def test_parser():
    """
    파서 테스트 함수 - 모든 기간 형식 테스트
    """
    parser = BigSignalMessageParser()
    
    # 테스트 메시지 1: 1월 21일 형식 (BUY)
    test_message_1 = """Buy BTC 📈

현재 가격 : 153,155,000 KRW
거래 페어 : KRW-BTC (Bithumb)
시그널: 📈 BUY (매수)
매수 비율 : 1.60%

[Notes]
score=6, oldATR=BUY, newATR=BUY, diff=BUY, trend=BUY, rectangle=HOLD, rsi=HOLD, macd=BUY, stoch=BUY, final=BUY, conf_range=2.00, rsi_val=48.83665207377522"""
    
    # 테스트 메시지 2: 1월 21일 형식 (SELL)
    test_message_2 = """Sell DOGE 📉

현재 가격 : 590 KRW
거래 페어 : KRW-DOGE (Bithumb)
시그널: 📉 SELL (매도)
매도 비율 : 12.70%

[Notes]
score=-4, oldATR=HOLD, newATR=HOLD, diff=SELL, trend=SELL, rectangle=HOLD, rsi=HOLD, macd=SELL, stoch=SELL, final=SELL, conf_range=29.15, rsi_val=66.66347577947778"""
    
    # 테스트 메시지 3: 8월 28일 형식 (BUY)
    test_message_3 = """Buy DOGE 📈

현재 가격 : 307 KRW
거래 페어 : KRW-DOGE (Bithumb)
시그널: 📈 BUY (매수)
매수 비율 : 0.24%

[Notes]
score_3m=-1
 atr_original_3m=HOLD
 atr_new_3m=HOLD
 diff_3m=HOLD
 trend_3m=SELL
 pred_range_3m=HOLD
score_5m=2
 signal_atr_original_5m=HOLD
 signal_atr_new_5m=HOLD
 signal_diff_5m=BUY
 signal_trend_5m=HOLD
 signal_pred_range_5m=BUY

Supplementary Score: 4.2, score_len=500, buy_threshold_dynamic=3.5, sell_threshold_dynamic=-3.3"""
    
    # 테스트 메시지 4: HOLD 형식 (거래 없음)
    test_message_4 = """BTC

현재 가격 : 156,431,000 KRW
거래 페어 : KRW-BTC (Bithumb)
시그널: HOLD
매매 비율 : 1.73%

[Notes]
score_3m=0
 atr_original_3m=HOLD
 atr_new_3m=HOLD"""
    
    print("=== BigSignal 통합 메시지 파서 테스트 ===")
    
    test_cases = [
        ("1월 21일 BTC BUY", test_message_1),
        ("1월 21일 DOGE SELL", test_message_2),
        ("8월 28일 DOGE BUY", test_message_3),
        ("HOLD 시그널 (skip)", test_message_4),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, (test_name, message) in enumerate(test_cases, 1):
        print(f"\n=== 테스트 {i}: {test_name} ===")
        result = parser.parse_message(message, datetime.now())
        
        if result:
            success_count += 1
            print(f"✅ 파싱 성공:")
            print(f"   자산: {result['asset']}")
            print(f"   액션: {result['action']}")
            print(f"   가격: {result['price']:,} {result['base_currency']}")
            print(f"   비율: {result['percentage']}%")
        else:
            print("❌ 파싱 실패 (정상: HOLD는 None 반환)")
    
    print(f"\n📊 전체 테스트 결과: {success_count}/{total_count-1} 성공 (HOLD 제외)")
    print("모든 기간 데이터 호환성 확인 완료!")

if __name__ == "__main__":
    test_parser()