#!/usr/bin/env python
"""
BigSignal 텔레그램 메시지 수집기
실시간으로 BigSignal 채널에서 메시지를 수집하여 거래 데이터로 변환
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Django 설정 추가
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from telethon import TelegramClient, events
from dotenv import load_dotenv
from trades.models import Trade
from decimal import Decimal

# 환경 변수 로드
load_dotenv()

# 로깅 설정 (인코딩 문제 해결)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_collector.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BigSignalCollector:
    """
    BigSignal 텔레그램 메시지 수집 및 처리
    """
    
    def __init__(self):
        # 텔레그램 API 설정
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone = os.getenv('TELEGRAM_PHONE')
        self.channel_id = int(os.getenv('TELEGRAM_CHANNEL_ID', 0))
        
        # 설정 검증
        if not all([self.api_id, self.api_hash, self.phone, self.channel_id]):
            raise ValueError("텔레그램 API 설정이 .env 파일에 없습니다")
        
        # 텔레그램 클라이언트 초기화
        self.client = TelegramClient('bigsignal_session', self.api_id, self.api_hash)
        
        # 메시지 파서 불러오기
        from scripts.message_parser import BigSignalMessageParser
        self.parser = BigSignalMessageParser()
        
        logger.info("BigSignal 수집기 초기화 완료")
    
    async def start(self):
        """
        텔레그램 클라이언트 시작 및 이벤트 핸들러 등록
        """
        logger.info("텔레그램 클라이언트 시작...")
        
        # 클라이언트 시작
        await self.client.start(phone=self.phone)
        
        # 채널 정보 확인
        try:
            channel = await self.client.get_entity(self.channel_id)
            logger.info(f"채널 연결 성공: {channel.title}")
        except Exception as e:
            logger.error(f"채널 연결 실패: {e}")
            return
        
        # 새 메시지 이벤트 핸들러 등록
        @self.client.on(events.NewMessage(chats=self.channel_id))
        async def handle_new_message(event):
            await self.process_message(event)
        
        logger.info("메시지 수집 시작...")
        logger.info("프로그램을 종료하려면 Ctrl+C를 누르세요")
        
        # 무한 실행
        await self.client.run_until_disconnected()
    
    async def process_message(self, event):
        """
        새로운 메시지 처리
        """
        try:
            message_text = event.message.message
            message_date = event.message.date
            
            logger.info(f"새 메시지 수신: {message_date}")
            logger.debug(f"메시지 내용: {message_text[:100]}...")
            
            # BigSignal 메시지인지 확인
            if not self.parser.is_valid_signal_message(message_text):
                logger.debug("BigSignal 메시지가 아님, 건너뜀")
                return
            
            # 메시지 파싱
            parsed_data = self.parser.parse_message(message_text, message_date)
            
            if parsed_data:
                # 데이터베이스에 저장
                await self.save_trade_data(parsed_data)
                logger.info(f"✅ 거래 데이터 저장 완료: {parsed_data['action']} {parsed_data['asset']}")
            else:
                logger.warning("메시지 파싱 실패")
                
        except Exception as e:
            logger.error(f"메시지 처리 중 오류: {e}")
    
    async def save_trade_data(self, parsed_data):
        """
        파싱된 데이터를 데이터베이스에 저장
        """
        try:
            # 중복 거래 확인 (같은 시간, 자산, 액션)
            existing_trade = Trade.objects.filter(
                timestamp=parsed_data['timestamp'],
                asset=parsed_data['asset'],
                action=parsed_data['action']
            ).first()
            
            if existing_trade:
                logger.warning("중복 거래 발견, 건너뜀")
                return
            
            # 새 거래 생성
            trade = Trade.objects.create(
                timestamp=parsed_data['timestamp'],
                asset=parsed_data['asset'],
                action=parsed_data['action'],
                price=Decimal(str(parsed_data['price'])),
                percentage=Decimal(str(parsed_data['percentage'])),
                base_currency=parsed_data['base_currency'],
                raw_message=parsed_data['raw_message']
            )
            
            logger.info(f"거래 저장 완료: ID={trade.id}")
            
            # 포트폴리오는 Django 신호를 통해 자동 업데이트됨
            
        except Exception as e:
            logger.error(f"데이터베이스 저장 실패: {e}")
    
    async def test_connection(self):
        """
        연결 테스트 - 여러 방법으로 채널 접근 시도
        """
        logger.info("연결 테스트 시작...")
        
        await self.client.start(phone=self.phone)
        
        try:
            # 방법 1: 직접 ID로 접근
            logger.info(f"방법 1: 채널 ID {self.channel_id}로 직접 접근...")
            channel = await self.client.get_entity(self.channel_id)
            
        except Exception as e1:
            logger.warning(f"방법 1 실패: {e1}")
            
            try:
                # 방법 2: 슈퍼그룹 ID 변환 후 접근
                if str(self.channel_id).startswith('-100'):
                    entity_id = int(str(self.channel_id).replace('-100', '-'))
                    logger.info(f"방법 2: 변환된 ID {entity_id}로 접근...")
                    channel = await self.client.get_entity(entity_id)
                else:
                    raise e1
                    
            except Exception as e2:
                logger.warning(f"방법 2 실패: {e2}")
                
                try:
                    # 방법 3: username 방식 (만약 있다면)
                    logger.info("방법 3: 가입한 채널 중에서 BigSignal 찾기...")
                    channel = None
                    async for dialog in self.client.iter_dialogs():
                        if 'bigsignal' in dialog.name.lower() or 'big' in dialog.name.lower():
                            channel = dialog.entity
                            logger.info(f"BigSignal 관련 채널 발견: {dialog.name}")
                            break
                    
                    if not channel:
                        raise Exception("BigSignal 채널을 찾을 수 없습니다")
                        
                except Exception as e3:
                    logger.error(f"모든 방법 실패: {e3}")
                    logger.error("해결책:")
                    logger.error("1. BigSignal 채널에 가입되어 있는지 확인")
                    logger.error("2. 채널 관리자에게 접근 권한 요청")
                    logger.error("3. 채널의 정확한 username이나 invite link 확인")
                    return
        
        # 연결 성공
        logger.info(f"채널 연결 성공: {channel.title}")
        logger.info(f"채널 ID: {channel.id}")
        logger.info(f"참가자 수: {getattr(channel, 'participants_count', '알 수 없음')}")
        
        # 최근 메시지 확인
        try:
            messages = await self.client.get_messages(channel, limit=3)
            logger.info(f"최근 메시지 {len(messages)}개 조회 성공")
            
            for i, msg in enumerate(messages, 1):
                if msg.message:
                    preview = msg.message[:50].replace('\n', ' ')
                    logger.info(f"메시지 {i}: {msg.date} - {preview}...")
                    
                    # BigSignal 메시지 테스트
                    if self.parser.is_valid_signal_message(msg.message):
                        logger.info(f"  -> BigSignal 거래 메시지 감지!")
                        
        except Exception as e:
            logger.warning(f"메시지 조회 실패: {e}")
        
        await self.client.disconnect()

async def main():
    """
    메인 함수
    """
    collector = BigSignalCollector()
    
    # 명령행 인수 확인
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # 테스트 모드
        await collector.test_connection()
    else:
        # 실제 수집 모드
        try:
            await collector.start()
        except KeyboardInterrupt:
            logger.info("사용자에 의해 종료됨")
        except Exception as e:
            logger.error(f"예기치 않은 오류: {e}")

if __name__ == "__main__":
    print("=== BigSignal 텔레그램 수집기 ===")
    print("실시간 메시지 수집 및 포트폴리오 업데이트")
    print("=" * 40)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n프로그램이 종료되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
        sys.exit(1)