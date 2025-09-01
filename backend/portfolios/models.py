"""
포트폴리오 관련 모델
"""
CLASS Portfolio(Model):
    FIELDS:
        - id: AutoField
        - name: CharField (BTC_Only, BTC_USDT 등)
        - description: TextField
        - assets: JSONField (['BTC', 'USDT'])
        - initial_budget: DecimalField (1000000)
        - current_value: DecimalField
        - pnl_absolute: DecimalField
        - pnl_percentage: DecimalField
        - cash_balance: DecimalField
        - holdings: JSONField ({'BTC': 0.1, 'USDT': 1000})
        - last_updated: DateTimeField
        - is_active: BooleanField
    
    METHODS:
        - calculate_current_value(): 현재 포트폴리오 가치 계산
        - get_asset_allocation(): 자산 배분 비율 반환
        - update_holdings(): 보유 자산 업데이트

CLASS PortfolioSnapshot(Model):
    FIELDS:
        - portfolio: ForeignKey to Portfolio
        - timestamp: DateTimeField
        - portfolio_value: DecimalField
        - pnl_percentage: DecimalField
        - cash_balance: DecimalField
        - holdings: JSONField
        - trade_triggered_by: ForeignKey to Trade (optional)
    
    META:
        - ordering: ['-timestamp']
        - indexes: ['timestamp', 'portfolio']