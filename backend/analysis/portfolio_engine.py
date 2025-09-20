from django.conf import settings
from django.utils import timezone
from portfolios.models import Portfolio, PortfolioSnapshot
from trades.models import Trade
from decimal import Decimal, ROUND_HALF_UP
import logging

logger = logging.getLogger(__name__)

class PortfolioEngine:
    """
    포트폴리오 시뮬레이션 엔진
    텔레그램 시그널에 따라 7가지 포트폴리오의 가상 거래 실행
    """
    
    def __init__(self):
        self.initial_budget = Decimal(str(settings.INITIAL_PORTFOLIO_BUDGET))
        self.portfolio_configs = settings.PORTFOLIO_CONFIGS
        self.supported_assets = settings.SUPPORTED_ASSETS
    
    def initialize_portfolios(self):
        """
        7가지 포트폴리오 초기 생성
        """
        created_count = 0
        
        for config in self.portfolio_configs:
            portfolio, created = Portfolio.objects.get_or_create(
                name=config['name'],
                defaults={
                    'description': f"{', '.join(config['assets'])} 자산 조합 포트폴리오",
                    'assets': config['assets'],
                    'initial_budget': self.initial_budget,
                    'current_value': self.initial_budget,
                    'cash_balance': self.initial_budget,
                    'holdings': {asset: Decimal('0') for asset in config['assets']},  # Decimal로 변경
                    'pnl_absolute': Decimal('0'),  # Decimal로 변경
                    'pnl_percentage': Decimal('0'),  # Decimal로 변경
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                logger.info(f"포트폴리오 생성: {portfolio.name}")
                
                # 초기 스냅샷 생성
                self.create_snapshot(portfolio, timezone.now(), None)
        
        logger.info(f"포트폴리오 초기화 완료: {created_count}개 생성")
        return Portfolio.objects.filter(is_active=True)
    
    def simulate_trade(self, trade):
        """
        새로운 거래에 대해 모든 포트폴리오 시뮬레이션 실행
        """
        if trade.asset not in self.supported_assets:
            logger.warning(f"지원하지 않는 자산: {trade.asset}")
            return
        
        portfolios = Portfolio.objects.filter(is_active=True)
        executed_count = 0
        
        for portfolio in portfolios:
            if self.execute_trade_for_portfolio(portfolio, trade):
                executed_count += 1
        
        logger.info(f"거래 시뮬레이션 완료: {trade} - {executed_count}개 포트폴리오 업데이트")
    
    def execute_trade_for_portfolio(self, portfolio, trade):
        """
        특정 포트폴리오에서 거래 실행
        """
        # 이 포트폴리오가 해당 자산을 거래하는지 확인
        if trade.asset not in portfolio.assets:
            return False
        
        trade_executed = False
        
        if trade.action == 'BUY':
            trade_executed = self.execute_buy(portfolio, trade)
        elif trade.action == 'SELL':
            trade_executed = self.execute_sell(portfolio, trade)
        
        if trade_executed:
            # 포트폴리오 가치 업데이트
            self.update_portfolio_value(portfolio, trade)
            
            # 스냅샷 생성
            self.create_snapshot(portfolio, trade.timestamp, trade)
            
            portfolio.save()
        
        return trade_executed
    
    def execute_buy(self, portfolio, trade):
        """
        매수 거래 실행
        """
        available_cash = portfolio.cash_balance
        trade_percentage = Decimal(str(trade.percentage))  # Decimal로 변환
        
        # 매수할 금액 계산 (모든 계산을 Decimal로)
        trade_amount = available_cash * (trade_percentage / Decimal('100'))
        
        # 현금이 충분한지 확인
        if trade_amount > available_cash:
            trade_amount = available_cash
        
        # 최소 거래 금액 체크 (1 KRW)
        if trade_amount < Decimal('1'):
            logger.debug(f"매수 금액이 너무 적음: {trade_amount} KRW")
            return False
        
        # 매수 수량 계산
        if trade.price > 0:
            quantity_bought = trade_amount / Decimal(str(trade.price))
            
            # 보유 자산 업데이트 (Decimal 타입 통일)
            current_holding = Decimal(str(portfolio.holdings.get(trade.asset, 0)))
            portfolio.holdings[trade.asset] = current_holding + quantity_bought
            
            # 현금 차감
            portfolio.cash_balance -= trade_amount
            
            logger.debug(f"매수 실행 - {portfolio.name}: {quantity_bought:.8f} {trade.asset} @ {trade.price:,} KRW")
            return True
        
        return False
    
    def execute_sell(self, portfolio, trade):
        """
        매도 거래 실행
        """
        current_holding = Decimal(str(portfolio.holdings.get(trade.asset, 0)))
        trade_percentage = Decimal(str(trade.percentage))  # Decimal로 변환
        
        # 매도할 수량 계산 (모든 계산을 Decimal로)
        quantity_to_sell = current_holding * (trade_percentage / Decimal('100'))
        
        # 보유 수량이 충분한지 확인
        if quantity_to_sell > current_holding:
            quantity_to_sell = current_holding
        
        # 최소 매도 수량 체크
        if quantity_to_sell <= Decimal('0.00000001'):  # 매우 작은 수량
            logger.debug(f"매도 수량이 너무 적음: {quantity_to_sell}")
            return False
        
        # 매도 대금 계산
        if trade.price > 0:
            sell_amount = quantity_to_sell * Decimal(str(trade.price))
            
            # 보유 자산 업데이트
            portfolio.holdings[trade.asset] = current_holding - quantity_to_sell
            
            # 현금 추가
            portfolio.cash_balance += sell_amount
            
            logger.debug(f"매도 실행 - {portfolio.name}: {quantity_to_sell:.8f} {trade.asset} @ {trade.price:,} KRW")
            return True
        
        return False
    
    def update_portfolio_value(self, portfolio, trade):
        """
        포트폴리오 총 가치 및 손익 업데이트
        """
        # 현재 시점의 자산 가격들 수집 (각 자산의 최신 거래 가격 사용)
        current_prices = self.get_current_prices(trade.timestamp)
        
        # 총 가치 계산: 현금 + (각 자산 보유량 × 현재가)
        total_value = portfolio.cash_balance
        
        for asset, quantity in portfolio.holdings.items():
            quantity_decimal = Decimal(str(quantity))  # Decimal로 변환
            if quantity_decimal > 0:
                asset_price = Decimal(str(current_prices.get(asset, 0)))
                total_value += quantity_decimal * asset_price
        
        # 값 업데이트 (모든 계산 결과를 Decimal로)
        portfolio.current_value = total_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        portfolio.pnl_absolute = portfolio.current_value - portfolio.initial_budget
        
        if portfolio.initial_budget > 0:
            portfolio.pnl_percentage = (portfolio.pnl_absolute / portfolio.initial_budget * Decimal('100')).quantize(
                Decimal('0.0001'), rounding=ROUND_HALF_UP
            )
        else:
            portfolio.pnl_percentage = Decimal('0')
        
        portfolio.last_updated = timezone.now()
    
    def get_current_prices(self, timestamp):
        """
        주어진 시점의 각 자산 가격 조회
        해당 시점 이전의 가장 최근 거래 가격 사용
        """
        prices = {}
        
        for asset in self.supported_assets:
            latest_trade = Trade.objects.filter(
                asset=asset,
                timestamp__lte=timestamp
            ).first()
            
            if latest_trade:
                prices[asset] = latest_trade.price
            else:
                prices[asset] = Decimal('0')  # Decimal로 변경
        
        return prices
    
    def create_snapshot(self, portfolio, timestamp, triggering_trade=None):
        """
        포트폴리오 스냅샷 생성
        """
        # holdings를 Decimal에서 float로 변환 (JSON 저장용)
        holdings_for_json = {k: float(v) for k, v in portfolio.holdings.items()}
        
        snapshot = PortfolioSnapshot.objects.create(
            portfolio=portfolio,
            timestamp=timestamp,
            portfolio_value=portfolio.current_value,
            pnl_percentage=portfolio.pnl_percentage,
            cash_balance=portfolio.cash_balance,
            holdings=holdings_for_json,  # float로 변환된 딕셔너리
            trade_triggered_by=triggering_trade
        )
        
        logger.debug(f"스냅샷 생성: {snapshot}")
        return snapshot
    
    def reset_portfolio(self, portfolio):
        """
        포트폴리오를 초기 상태로 리셋
        """
        portfolio.current_value = portfolio.initial_budget
        portfolio.cash_balance = portfolio.initial_budget
        portfolio.holdings = {asset: Decimal('0') for asset in portfolio.assets}  # Decimal로 변경
        portfolio.pnl_absolute = Decimal('0')  # Decimal로 변경
        portfolio.pnl_percentage = Decimal('0')  # Decimal로 변경
        portfolio.last_updated = timezone.now()
        portfolio.save()
        
        # 기존 스냅샷 삭제
        portfolio.snapshots.all().delete()
        
        # 초기 스냅샷 생성
        self.create_snapshot(portfolio, timezone.now(), None)
        
        logger.info(f"포트폴리오 리셋: {portfolio.name}")
    
    def recalculate_all_portfolios(self):
        """
        모든 거래를 다시 재생해서 포트폴리오 재계산
        """
        logger.info("전체 포트폴리오 재계산 시작...")
        
        # 모든 포트폴리오 초기화
        portfolios = Portfolio.objects.filter(is_active=True)
        for portfolio in portfolios:
            self.reset_portfolio(portfolio)
        
        # 시간 순으로 모든 거래 재실행
        trades = Trade.objects.all().order_by('timestamp')
        processed_count = 0
        
        for trade in trades:
            self.simulate_trade(trade)
            processed_count += 1
            
            if processed_count % 100 == 0:
                logger.info(f"거래 처리 진행률: {processed_count}/{trades.count()}")
        
        logger.info(f"전체 포트폴리오 재계산 완료: {processed_count}건 처리")
    
    def get_portfolio_performance_data(self, portfolio_name, days=30):
        """
        특정 포트폴리오의 성과 데이터 반환 (차트용)
        """
        from datetime import timedelta
        
        try:
            portfolio = Portfolio.objects.get(name=portfolio_name, is_active=True)
        except Portfolio.DoesNotExist:
            return []
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        snapshots = portfolio.snapshots.filter(
            timestamp__gte=start_date,
            timestamp__lte=end_date
        ).order_by('timestamp')
        
        performance_data = []
        for snapshot in snapshots:
            performance_data.append({
                'timestamp': snapshot.timestamp.isoformat(),
                'portfolio_value': float(snapshot.portfolio_value),
                'pnl_percentage': float(snapshot.pnl_percentage),
                'cash_balance': float(snapshot.cash_balance),
                'holdings': snapshot.holdings
            })
        
        return performance_data
    
    def get_all_portfolios_summary(self):
        """
        모든 포트폴리오의 현재 상태 요약
        """
        portfolios = Portfolio.objects.filter(is_active=True).order_by('name')
        summary = {}
        
        for portfolio in portfolios:
            summary[portfolio.name] = {
                'name': portfolio.name,
                'description': portfolio.description,
                'assets': portfolio.assets,
                'current_value': float(portfolio.current_value),
                'pnl_absolute': float(portfolio.pnl_absolute),
                'pnl_percentage': float(portfolio.pnl_percentage),
                'cash_balance': float(portfolio.cash_balance),
                'holdings': {k: float(v) for k, v in portfolio.holdings.items()},
                'last_updated': portfolio.last_updated.isoformat()
            }
        
        return summary


# 유틸리티 함수들
def process_new_trade(trade_instance):
    """
    새로운 거래 발생 시 포트폴리오 엔진 실행
    """
    engine = PortfolioEngine()
    engine.simulate_trade(trade_instance)

def initialize_system():
    """
    시스템 초기화 (포트폴리오 생성)
    """
    engine = PortfolioEngine()
    return engine.initialize_portfolios()

def recalculate_system():
    """
    전체 시스템 재계산
    """
    engine = PortfolioEngine()
    engine.recalculate_all_portfolios()

def get_portfolio_chart_data(portfolio_name, days=30):
    """
    차트용 포트폴리오 데이터 반환
    """
    engine = PortfolioEngine()
    return engine.get_portfolio_performance_data(portfolio_name, days)