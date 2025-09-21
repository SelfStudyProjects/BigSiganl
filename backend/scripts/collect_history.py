#!/usr/bin/env python
"""
BigSignal 과거 메시지 일괄 수집기
텔레그램 채널의 모든 과거 메시지를 수집하여 거래 데이터로 변환
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from telethon import TelegramClient
from dotenv import load_dotenv
from trades.models import Trade
from decimal import Decimal
import logging

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('historical_collector.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class HistoricalCollector:
    """
    과거 BigSignal 메시지 일괄 수집
    """
    
    def __init__(self):
        # 텔레그램 API 설정
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone = os.getenv('TELEGRAM_PHONE')
        self.channel_id = int(os.getenv('TELEGRAM_CHANNEL_ID', 0))
        
        # 텔레그램 클라이언트 초기화
        self.client = TelegramClient('historical_session', self.api_id, self.api_hash)
        
        # 메시지 파서
        from scripts.message_parser import BigSignalMessageParser
        self.parser = BigSignalMessageParser()
        
        # 통계
        self.stats = {
            'total_messages': 0,
            'signal_messages': 0,
            'parsed_successfully': 0,
            'saved_trades': 0,
            'duplicates': 0,
            'errors': 0
        }
    
    async def collect_all_history(self, days_back=365):
        """
        지정된 일수만큼 과거 메시지 수집
        """
        logger.info(f"과거 {days_back}일간의 BigSignal 메시지 수집 시작...")
        
        await self.client.start(phone=self.phone)
        
        try:
            # 채널 연결
            channel = await self.client.get_entity(self.channel_id)
            logger.info(f"채널 연결: {channel.title}")
            
            # 수집 기간 설정 (timezone 문제 해결)
            from django.utils import timezone as django_timezone
            
            end_date = django_timezone.now()
            start_date = end_date - timedelta(days=days_back)
            
            # timezone-aware로 변환
            if start_date.tzinfo is None:
                start_date = start_date.replace(tzinfo=django_timezone.utc)
            if end_date.tzinfo is None:
                end_date = end_date.replace(tzinfo=django_timezone.utc)
            
            logger.info(f"수집 기간: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
            
            # 모든 메시지 수집 (개선된 로직)
            collected_messages = []
            
            # 먼저 전체 메시지 개수 확인
            total_count = 0
            async for message in self.client.iter_messages(channel, limit=None):
                total_count += 1
                if total_count % 50 == 0:
                    logger.info(f"전체 메시지 스캔 중: {total_count}개...")
                if total_count >= 1000:  # 최대 1000개로 제한
                    break
            
            logger.info(f"채널의 총 메시지 수: {total_count}개")
            
            # 실제 수집 (최신 메시지부터)
            collected_count = 0
            async for message in self.client.iter_messages(channel, limit=total_count):
                self.stats['total_messages'] += 1
                
                # message.date가 timezone-aware인지 확인
                msg_date = message.date
                if msg_date.tzinfo is None:
                    msg_date = msg_date.replace(tzinfo=django_timezone.utc)
                
                # 기간 필터링
                if msg_date < start_date:
                    continue
                if msg_date > end_date:
                    continue
                
                if message.message:
                    collected_messages.append(message)
                    collected_count += 1
                    
                    # 샘플 메시지 출력
                    if collected_count <= 3:
                        preview = message.message[:50].replace('\n', ' ')
                        logger.info(f"수집된 메시지 예시 {collected_count}: {msg_date} - {preview}...")
                    
                # 진행 상황 출력
                if self.stats['total_messages'] % 20 == 0:
                    logger.info(f"수집 진행: {self.stats['total_messages']}개 스캔, {collected_count}개 수집")
            
            logger.info(f"총 {len(collected_messages)}개 메시지 수집 완료")
            
            # 메시지 처리
            await self.process_messages(collected_messages)
            
        except Exception as e:
            logger.error(f"수집 중 오류: {e}")
            self.stats['errors'] += 1
        
        finally:
            await self.client.disconnect()
            self.print_statistics()
    
    async def process_messages(self, messages):
        """
        수집된 메시지들을 처리하여 거래 데이터 생성
        """
        logger.info("메시지 처리 시작...")
        
        for i, message in enumerate(messages, 1):
            try:
                # BigSignal 메시지인지 확인
                if not self.parser.is_valid_signal_message(message.message):
                    continue
                
                self.stats['signal_messages'] += 1
                logger.info(f"[{i}/{len(messages)}] BigSignal 메시지 발견: {message.date}")
                
                # 메시지 파싱
                parsed_data = self.parser.parse_message(message.message, message.date)
                
                if parsed_data:
                    self.stats['parsed_successfully'] += 1
                    
                    # 중복 확인 및 저장
                    if await self.save_trade_data(parsed_data):
                        self.stats['saved_trades'] += 1
                        logger.info(f"  -> 거래 저장: {parsed_data['action']} {parsed_data['asset']} ({parsed_data['percentage']}%)")
                    else:
                        self.stats['duplicates'] += 1
                        logger.debug("  -> 중복 거래, 건너뜀")
                else:
                    logger.warning(f"  -> 파싱 실패: {message.message[:50]}...")
                
            except Exception as e:
                logger.error(f"메시지 처리 오류: {e}")
                self.stats['errors'] += 1
    
    async def save_trade_data(self, parsed_data):
        """
        파싱된 데이터를 데이터베이스에 저장 (async 지원)
        """
        from django.db import transaction
        from asgiref.sync import sync_to_async
        
        try:
            # async 환경에서 Django ORM 사용
            @sync_to_async
            def check_existing():
                return Trade.objects.filter(
                    timestamp=parsed_data['timestamp'],
                    asset=parsed_data['asset'],
                    action=parsed_data['action'],
                    price=Decimal(str(parsed_data['price']))
                ).exists()
            
            @sync_to_async
            def create_trade():
                return Trade.objects.create(
                    timestamp=parsed_data['timestamp'],
                    asset=parsed_data['asset'],
                    action=parsed_data['action'],
                    price=Decimal(str(parsed_data['price'])),
                    percentage=Decimal(str(parsed_data['percentage'])),
                    base_currency=parsed_data['base_currency'],
                    raw_message=parsed_data['raw_message']
                )
            
            # 중복 확인
            if await check_existing():
                return False  # 중복
            
            # 새 거래 생성
            trade = await create_trade()
            return True  # 저장 성공
            
        except Exception as e:
            logger.error(f"데이터베이스 저장 실패: {e}")
            return False
    
    def print_statistics(self):
        """
        수집 통계 출력
        """
        logger.info("=" * 50)
        logger.info("📊 수집 완료 통계")
        logger.info("=" * 50)
        logger.info(f"총 메시지 수집: {self.stats['total_messages']:,}개")
        logger.info(f"BigSignal 메시지: {self.stats['signal_messages']:,}개")
        logger.info(f"파싱 성공: {self.stats['parsed_successfully']:,}개")
        logger.info(f"거래 저장: {self.stats['saved_trades']:,}개")
        logger.info(f"중복 건너뜀: {self.stats['duplicates']:,}개")
        logger.info(f"오류 발생: {self.stats['errors']:,}개")
        logger.info("=" * 50)
        
        if self.stats['saved_trades'] > 0:
            logger.info(f"✅ 총 {self.stats['saved_trades']}개의 거래 데이터가 추가되었습니다")
            logger.info("포트폴리오 재계산을 실행하세요: python manage.py shell")
            logger.info(">>> from analysis.portfolio_engine import recalculate_system")
            logger.info(">>> recalculate_system()")

async def main():
    """
    메인 함수
    """
    collector = HistoricalCollector()
    
    # 명령행 인수로 일수 지정 가능
    days_back = 365  # 기본 1년
    if len(sys.argv) > 1:
        try:
            days_back = int(sys.argv[1])
        except ValueError:
            logger.warning("잘못된 일수 형식, 기본값 365일 사용")
    
    logger.info(f"BigSignal 과거 메시지 수집 시작 (최근 {days_back}일)")
    await collector.collect_all_history(days_back)

if __name__ == "__main__":
    print("=== BigSignal 과거 메시지 일괄 수집기 ===")
    print("사용법: python collect_history.py [일수]")
    print("예시: python collect_history.py 30  # 최근 30일")
    print("=" * 40)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n수집이 중단되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
        sys.exit(1)