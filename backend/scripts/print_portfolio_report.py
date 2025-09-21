#!/usr/bin/env python
"""
간단한 리포트 스크립트: 거래 수, 첫/마지막 거래, 포트폴리오 상태, 자산별 거래 수 출력
사용법:
  cd backend
  .\.venv\Scripts\python.exe scripts\print_portfolio_report.py
"""
import os
import sys
from pathlib import Path

# Django project root을 경로에 추가
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from trades.models import Trade
from portfolios.models import Portfolio
from django.db.models import Count


def main():
    print('# BigSignal 간단 리포트')
    print('\n# 1. 거래 데이터 확인')
    print(f"총 거래 수: {Trade.objects.count()}")
    first = Trade.objects.first()
    last = Trade.objects.last()
    print(f"첫 거래: {first.timestamp if first else '없음'}")
    print(f"마지막 거래: {last.timestamp if last else '없음'}")

    print('\n# 2. 포트폴리오 현황 확인')
    for p in Portfolio.objects.all():
        # p.current_value는 DecimalField, profit_loss_percentage는 추가된 프로퍼티
        try:
            cv = float(p.current_value)
        except Exception:
            cv = 0.0
        try:
            plp = float(p.profit_loss_percentage)
        except Exception:
            plp = 0.0
        print(f"{p.name}: ${cv:,.2f} ({plp:.2f}%)")

    print('\n# 3. 자산별 거래 수 확인')
    trades_by_asset = Trade.objects.values('asset').annotate(count=Count('id'))
    for item in trades_by_asset:
        print(f"{item['asset']}: {item['count']}개 거래")


if __name__ == '__main__':
    main()
