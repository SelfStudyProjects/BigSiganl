"""
거래 데이터 모델
"""
CLASS Trade(Model):
    FIELDS:
        - id: AutoField
        - timestamp: DateTimeField (거래 시점)
        - asset: CharField (BTC, USDT, DOGE)
        - action: CharField (BUY, SELL)
        - price: DecimalField (거래 가격)
        - percentage: DecimalField (매매 비율)
        - base_currency: CharField (KRW)
        - raw_message: TextField (원본 텔레그램 메시지)
        - created_at: DateTimeField
    
    METHODS:
        - __str__(): RETURN "{action} {asset} at {price}"
        - get_absolute_url(): RETURN trade detail URL
    
    META:
        - ordering: ['-timestamp']
        - indexes: ['timestamp', 'asset', 'action']