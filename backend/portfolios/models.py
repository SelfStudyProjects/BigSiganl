from django.db import models
from trades.models import Trade

"""
포트폴리오 관련 모델
"""
class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text="BTC_Only, BTC_USDT 등")
    description = models.TextField(blank=True)
    assets = models.JSONField(default=list, help_text="['BTC', 'USDT']")
    initial_budget = models.DecimalField(max_digits=15, decimal_places=2, default=1000000)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, default=1000000)  # default 추가
    pnl_absolute = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # default 추가
    pnl_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # default 추가
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=1000000)  # default 추가
    holdings = models.JSONField(default=dict, help_text="{'BTC': 0.1, 'USDT': 1000}")
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def calculate_current_value(self):
        # 현재 포트폴리오 가치 계산
        pass
    
    def get_asset_allocation(self):
        # 자산 배분 비율 반환
        pass
    
    def update_holdings(self):
        # 보유 자산 업데이트
        pass

class PortfolioSnapshot(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='snapshots')
    timestamp = models.DateTimeField()
    portfolio_value = models.DecimalField(max_digits=15, decimal_places=2)
    pnl_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2)
    holdings = models.JSONField(default=dict)
    trade_triggered_by = models.ForeignKey(Trade, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['portfolio']),
        ]
    
    def __str__(self):
        return f"{self.portfolio.name} at {self.timestamp}"