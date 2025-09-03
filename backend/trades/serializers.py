# from rest_framework import serializers
from .models import Trade

"""
거래 데이터 시리얼라이저 (DRF 없이 사용하지 않음)
"""
# class TradeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Trade
#         fields = '__all__'
#
#     def validate_price(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Price must be greater than 0")
#         return value
#
#     def validate_percentage(self, value):
#         if value < 0 or value > 100:
#             raise serializers.ValidationError("Percentage must be between 0 and 100")
#         return value

# class TradeCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Trade
#         exclude = ['created_at']
#
#     def create(self, validated_data):
#         return Trade.objects.create(**validated_data)