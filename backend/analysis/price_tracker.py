from django.utils import timezone
from trades.models import Trade, PriceHistory
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class PriceTracker:
    """
    Trade 데이터를 기반으로 자산별 가격 변동 추정
    """
    
    def __init__(self):
        self.supported_assets = ['BTC', 'USDT', 'DOGE', 'USDC']
    
    def process_new_trade(self, trade):
        """
        새로운 거래가 발생했을 때 가격 이력 업데이트
        """
        if trade.asset not in self.supported_assets:
            logger.warning(f"지원하지 않는 자산: {trade.asset}")
            return None
        
        # 이전 가격 찾기
        previous_price = self.get_previous_price(trade.asset, trade.timestamp)
        
        # 가격 변동 계산
        current_price = trade.price
        price_change = current_price - previous_price if previous_price > 0 else Decimal('0')
        price_change_percentage = (price_change / previous_price * 100) if previous_price > 0 else Decimal('0')
        
        # 거래량 지표 (거래 비율을 거래량의 대리 지표로 사용)
        volume_indicator = trade.percentage
        
        # PriceHistory 생성
        price_history = PriceHistory.objects.create(
            asset=trade.asset,
            timestamp=trade.timestamp,
            price=current_price,
            price_change=price_change,
            price_change_percentage=price_change_percentage,
            volume_indicator=volume_indicator,
            source_trade=trade
        )
        
        logger.info(f"가격 이력 생성: {price_history}")
        return price_history
    
    def get_previous_price(self, asset, current_timestamp):
        """
        특정 자산의 이전 가격 찾기
        """
        previous_record = PriceHistory.objects.filter(
            asset=asset,
            timestamp__lt=current_timestamp
        ).first()
        
        if previous_record:
            return previous_record.price
        
        # 이전 기록이 없으면 Trade에서 찾기
        previous_trade = Trade.objects.filter(
            asset=asset,
            timestamp__lt=current_timestamp
        ).first()
        
        return previous_trade.price if previous_trade else Decimal('0')
    
    def calculate_daily_return(self, asset, date):
        """
        특정 날짜의 일간 수익률 계산
        """
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # 하루 시작 가격
        start_price = self.get_price_at_time(asset, start_of_day)
        # 하루 끝 가격  
        end_price = self.get_price_at_time(asset, end_of_day)
        
        if start_price > 0:
            daily_return = (end_price - start_price) / start_price * 100
            return float(daily_return)
        
        return 0.0
    
    def get_price_at_time(self, asset, timestamp):
        """
        특정 시점의 가격 반환 (가장 가까운 이전 시점)
        """
        price_record = PriceHistory.objects.filter(
            asset=asset,
            timestamp__lte=timestamp
        ).first()
        
        if price_record:
            return price_record.price
        
        # PriceHistory에 없으면 Trade에서 찾기
        trade_record = Trade.objects.filter(
            asset=asset,
            timestamp__lte=timestamp
        ).first()
        
        return trade_record.price if trade_record else Decimal('0')
    
    def get_asset_performance_data(self, asset, days=30):
        """
        특정 자산의 성과 데이터 반환 (차트용)
        """
        from datetime import datetime, timedelta
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        price_records = PriceHistory.objects.filter(
            asset=asset,
            timestamp__gte=start_date,
            timestamp__lte=end_date
        ).order_by('timestamp')
        
        if not price_records.exists():
            return []
        
        # 첫 번째 가격을 기준점(100%)으로 설정
        first_price = price_records.first().price
        performance_data = []
        
        for record in price_records:
            if first_price > 0:
                return_percentage = (record.price - first_price) / first_price * 100
            else:
                return_percentage = 0
            
            performance_data.append({
                'timestamp': record.timestamp.isoformat(),
                'price': float(record.price),
                'return_percentage': float(return_percentage),
                'price_change_percentage': float(record.price_change_percentage)
            })
        
        return performance_data
    
    def backfill_price_history(self):
        """
        기존 Trade 데이터를 기반으로 PriceHistory 백필
        """
        logger.info("가격 이력 백필 시작...")
        
        for asset in self.supported_assets:
            trades = Trade.objects.filter(asset=asset).order_by('timestamp')
            
            for trade in trades:
                # 이미 존재하는지 확인
                existing = PriceHistory.objects.filter(
                    asset=asset,
                    source_trade=trade
                ).exists()
                
                if not existing:
                    self.process_new_trade(trade)
        
        logger.info("가격 이력 백필 완료")
    
    def get_latest_prices(self):
        """
        모든 자산의 최신 가격 반환
        """
        latest_prices = {}
        
        for asset in self.supported_assets:
            latest_record = PriceHistory.objects.filter(asset=asset).first()
            if latest_record:
                latest_prices[asset] = {
                    'price': float(latest_record.price),
                    'change_percentage': float(latest_record.price_change_percentage),
                    'timestamp': latest_record.timestamp.isoformat()
                }
            else:
                # PriceHistory가 없으면 Trade에서 찾기
                latest_trade = Trade.objects.filter(asset=asset).first()
                if latest_trade:
                    latest_prices[asset] = {
                        'price': float(latest_trade.price),
                        'change_percentage': 0.0,
                        'timestamp': latest_trade.timestamp.isoformat()
                    }
        
        return latest_prices


# 유틸리티 함수들
def update_price_on_new_trade(trade_instance):
    """
    새 거래 발생 시 호출되는 함수
    Trade 모델의 post_save 시그널에서 호출
    """
    tracker = PriceTracker()
    tracker.process_new_trade(trade_instance)

def get_asset_chart_data(asset, days=30):
    """
    차트용 자산 데이터 반환
    """
    tracker = PriceTracker()
    return tracker.get_asset_performance_data(asset, days)