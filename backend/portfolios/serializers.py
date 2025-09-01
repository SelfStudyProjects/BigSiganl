from rest_framework import serializers
from .models import Portfolio

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'  # Include all fields from the Portfolio model

class PortfolioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'created_at', 'updated_at']  # Specify fields for detailed view