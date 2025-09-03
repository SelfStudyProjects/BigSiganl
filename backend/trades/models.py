from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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