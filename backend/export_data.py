import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core import serializers
from trades.models import Trade

# UTF-8로 파일 쓰기
with open('trades_data.json', 'w', encoding='utf-8') as f:
    data = serializers.serialize('json', Trade.objects.all(), indent=2)
    f.write(data)

print("✓ trades_data.json created")