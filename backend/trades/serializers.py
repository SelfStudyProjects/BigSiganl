from rest_framework import serializers
from .models import Trade

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'  # or specify the fields you want to include, e.g., ['id', 'symbol', 'quantity', 'price', 'timestamp']