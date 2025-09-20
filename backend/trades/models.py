from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Trade(models.Model):
    """
    텔레그램에서 수집된 거래 시그널 데이터
    """
    ACTION_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    
    ASSET_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('USDT', 'Tether'),
        ('DOGE', 'Dogecoin'),
    ]
    
    timestamp = models.DateTimeField(
        verbose_name='거래 시점',
        help_text='텔레그램 메시지가 전송된 시점'
    )
    asset = models.CharField(
        max_length=10,
        choices=ASSET_CHOICES,
        verbose_name='자산명',
        help_text='거래 대상 암호화폐'
    )
    action = models.CharField(
        max_length=4,
        choices=ACTION_CHOICES,
        verbose_name='거래 행동',
        help_text='매수 또는 매도'
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='거래 가격',
        help_text='KRW 기준 거래 가격'
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)],
        verbose_name='거래 비율',
        help_text='매수/매도 비율 (%)'
    )
    base_currency = models.CharField(
        max_length=3,
        default='KRW',
        verbose_name='기준 통화',
        help_text='거래 가격의 기준 통화'
    )
    raw_message = models.TextField(
        verbose_name='원본 메시지',
        help_text='파싱 전 원본 텔레그램 메시지',
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성 시간'
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['asset']),
            models.Index(fields=['action']),
            models.Index(fields=['timestamp', 'asset']),
        ]
        verbose_name = '거래'
        verbose_name_plural = '거래 목록'
    
    def __str__(self):
        return f"{self.action} {self.asset} at {self.price:,} KRW ({self.percentage}%)"
    
    @property
    def is_buy(self):
        return self.action == 'BUY'
    
    @property
    def is_sell(self):
        return self.action == 'SELL'
    
    def get_trade_amount(self, available_balance):
        """
        주어진 잔고에서 실제 거래할 금액/수량 계산
        """
        return available_balance * (self.percentage / 100)
    
class PriceHistory(models.Model):
    """
    각 자산의 가격 변동 추적
    Trade 데이터를 기반으로 생성
    """
    ASSET_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('USDT', 'Tether'),
        ('DOGE', 'Dogecoin'),
        ('USDC', 'USD Coin'),
    ]
    
    asset = models.CharField(
        max_length=10,
        choices=ASSET_CHOICES,
        verbose_name='자산명'
    )
    timestamp = models.DateTimeField(
        verbose_name='시점',
        help_text='가격이 기록된 시점'
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='가격 (KRW)',
        help_text='해당 시점의 자산 가격'
    )
    price_change = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='가격 변동 (KRW)',
        help_text='이전 가격 대비 변동량'
    )
    price_change_percentage = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        default=0,
        verbose_name='가격 변동률 (%)',
        help_text='이전 가격 대비 변동률'
    )
    volume_indicator = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='거래량 지표',
        help_text='해당 시점의 거래 비율 (추정)'
    )
    source_trade = models.ForeignKey(
        Trade,
        on_delete=models.CASCADE,
        verbose_name='소스 거래',
        help_text='이 가격 데이터를 생성한 거래'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['asset', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
        unique_together = ['asset', 'timestamp', 'source_trade']
        verbose_name = '가격 이력'
        verbose_name_plural = '가격 이력 목록'
    
    def __str__(self):
        return f"{self.asset} at {self.timestamp.strftime('%m-%d %H:%M')} - {self.price:,} KRW ({self.price_change_percentage:+.2f}%)"
    
    @classmethod
    def get_latest_price(cls, asset):
        """특정 자산의 최신 가격 반환"""
        latest = cls.objects.filter(asset=asset).first()
        return float(latest.price) if latest else 0
    
    @classmethod 
    def get_price_at_time(cls, asset, timestamp):
        """특정 시점의 자산 가격 반환 (가장 가까운 이전 시점)"""
        price_record = cls.objects.filter(
            asset=asset,
            timestamp__lte=timestamp
        ).first()
        return float(price_record.price) if price_record else 0

# 포트폴리오 신호 처리 - 지연 import로 순환 참조 해결
@receiver(post_save, sender=Trade)
def process_new_trade_signal(sender, instance, created, **kwargs):
    if created:  # 새로 생성된 경우만
        import logging
        logger = logging.getLogger(__name__)
        
        # 1. 가격 이력 업데이트 (지연 import)
        try:
            from analysis.price_tracker import update_price_on_new_trade
            update_price_on_new_trade(instance)
        except ImportError:
            logger.warning("price_tracker 모듈을 찾을 수 없습니다")
        except Exception as e:
            logger.warning(f"가격 이력 업데이트 실패: {e}")
        
        # 2. 포트폴리오 시뮬레이션 실행 (지연 import)
        try:
            from analysis.portfolio_engine import process_new_trade
            process_new_trade(instance)
            logger.info(f"포트폴리오 처리 완료: {instance}")
        except ImportError as e:
            logger.error(f"portfolio_engine 모듈 import 실패: {e}")
        except Exception as e:
            logger.error(f"포트폴리오 처리 실패: {e}")