"""
거래 데이터 시리얼라이저
"""
CLASS TradeSerializer(ModelSerializer):
    FIELDS: all from Trade model
    
    METHOD validate_price():
        IF price <= 0:
            RAISE ValidationError
        RETURN price
    
    METHOD validate_percentage():
        IF percentage < 0 OR percentage > 100:
            RAISE ValidationError
        RETURN percentage

CLASS TradeCreateSerializer(ModelSerializer):
    FIELDS: exclude 'created_at'
    
    METHOD create():
        VALIDATE incoming data
        CREATE new Trade instance
        RETURN created instance