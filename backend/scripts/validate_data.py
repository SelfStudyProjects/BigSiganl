#!/usr/bin/env python
"""
데이터 검증 및 수정 스크립트
- 시간 순서 확인
- 중복 데이터 체크
- 포트폴리오 재계산
"""
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from trades.models import Trade
from portfolios.models import Portfolio, PortfolioSnapshot
from django.db.models import Count
from django.utils import timezone

def check_trade_data_integrity():
    """거래 데이터 무결성 검사"""
    print("=== 거래 데이터 무결성 검사 ===")
    
    # 1. 시간 순서 확인
    trades_by_time = Trade.objects.all().order_by('timestamp')
    trades_by_id = Trade.objects.all().order_by('id')
    
    print(f"총 거래 수: {trades_by_time.count()}")
    print(f"시간순 첫 거래: {trades_by_time.first().timestamp}")
    print(f"시간순 마지막 거래: {trades_by_time.last().timestamp}")
    print(f"ID순 첫 거래: {trades_by_id.first().timestamp}")
    print(f"ID순 마지막 거래: {trades_by_id.last().timestamp}")
    
    # 2. 중복 거래 확인
    duplicates = Trade.objects.values('timestamp', 'asset', 'action', 'price').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    print(f"\n중복 거래: {duplicates.count()}개")
    for dup in duplicates[:5]:  # 상위 5개만 표시
        print(f"  - {dup['timestamp']} {dup['asset']} {dup['action']} (중복 {dup['count']}개)")
    
    # 3. 자산별 가격 범위 확인
    print("\n자산별 가격 범위:")
    for asset in ['BTC', 'DOGE', 'USDT', 'USDC']:
        asset_trades = Trade.objects.filter(asset=asset)
        if asset_trades.exists():
            min_price = asset_trades.order_by('price').first().price
            max_price = asset_trades.order_by('-price').first().price
            print(f"  {asset}: {min_price:,} ~ {max_price:,} KRW ({asset_trades.count()}개 거래)")

def check_portfolio_consistency():
    """포트폴리오 일관성 검사"""
    print("\n=== 포트폴리오 일관성 검사 ===")
    
    for portfolio in Portfolio.objects.all():
        print(f"\n{portfolio.name}:")
        print(f"  현재 가치: {portfolio.current_value:,}")
        print(f"  초기 투자: {portfolio.initial_budget:,}")
        print(f"  손익: {portfolio.pnl_absolute:,}")
        print(f"  수익률: {portfolio.profit_loss_percentage:.2f}%")
        print(f"  현금 잔고: {portfolio.cash_balance:,}")
        print(f"  보유 자산: {portfolio.holdings}")
        
        # 수익률 계산 검증
        calculated_pnl = (float(portfolio.current_value) - float(portfolio.initial_budget)) / float(portfolio.initial_budget) * 100
        model_pnl = float(portfolio.profit_loss_percentage)
        
        if abs(calculated_pnl - model_pnl) > 0.01:
            print(f"  ⚠️ 수익률 불일치: 계산값 {calculated_pnl:.2f}% vs 모델값 {model_pnl:.2f}%")

def clean_duplicate_trades():
    """중복 거래 제거"""
    print("\n=== 중복 거래 제거 ===")
    
    # 정확히 동일한 거래 찾기 (timestamp, asset, action, price 모두 같음)
    seen_trades = set()
    duplicates_to_delete = []
    
    for trade in Trade.objects.all().order_by('timestamp', 'id'):
        trade_key = (trade.timestamp, trade.asset, trade.action, float(trade.price))
        
        if trade_key in seen_trades:
            duplicates_to_delete.append(trade.id)
            print(f"중복 발견: {trade.timestamp} {trade.asset} {trade.action}")
        else:
            seen_trades.add(trade_key)
    
    if duplicates_to_delete:
        print(f"삭제할 중복 거래: {len(duplicates_to_delete)}개")
        confirm = input("중복 거래를 삭제하시겠습니까? (y/N): ")
        if confirm.lower() == 'y':
            Trade.objects.filter(id__in=duplicates_to_delete).delete()
            print(f"✅ {len(duplicates_to_delete)}개 중복 거래 삭제 완료")
    else:
        print("✅ 중복 거래 없음")

def recalculate_all_portfolios():
    """모든 포트폴리오 재계산"""
    print("\n=== 포트폴리오 재계산 ===")
    
    try:
        # 실제 포트폴리오 엔진 사용
        from analysis.portfolio_engine import recalculate_system
        
        trades = Trade.objects.all().order_by('timestamp')
        print(f"총 {trades.count()}개 거래로 포트폴리오 재계산 시작...")
        
        # 실제 엔진 재계산 실행
        recalculate_system()
        print("✅ 포트폴리오 엔진으로 재계산 완료")
        
        # 결과 출력
        print("\n재계산 후 포트폴리오 현황:")
        for portfolio in Portfolio.objects.all():
            try:
                pnl_pct = float(portfolio.profit_loss_percentage)
            except:
                pnl_pct = 0.0
            print(f"{portfolio.name}: {pnl_pct:.2f}%")
            
    except Exception as e:
        print(f"❌ 포트폴리오 재계산 오류: {e}")
        import traceback
        traceback.print_exc()
        
        # 대안 제시
        print("\n대신 Django shell에서 직접 실행하세요:")
        print("python manage.py shell")
        print(">>> from analysis.portfolio_engine import recalculate_system")
        print(">>> recalculate_system()")

def generate_trade_timeline():
    """거래 타임라인 생성"""
    print("\n=== 거래 타임라인 ===")
    
    trades = Trade.objects.all().order_by('timestamp')
    
    if trades.count() == 0:
        print("거래 데이터가 없습니다.")
        return
    
    print(f"기간: {trades.first().timestamp} ~ {trades.last().timestamp}")
    
    # 월별 거래 수
    monthly_stats = {}
    for trade in trades:
        month_key = trade.timestamp.strftime('%Y-%m')
        if month_key not in monthly_stats:
            monthly_stats[month_key] = {'BUY': 0, 'SELL': 0}
        monthly_stats[month_key][trade.action] += 1
    
    print("\n월별 거래 통계:")
    for month, stats in sorted(monthly_stats.items()):
        total = stats['BUY'] + stats['SELL']
        print(f"  {month}: {total}개 (BUY: {stats['BUY']}, SELL: {stats['SELL']})")

def main():
    """메인 함수"""
    print("BigSignal 데이터 검증 및 수정 도구")
    print("=" * 50)
    
    # 1. 데이터 무결성 검사
    check_trade_data_integrity()
    
    # 2. 포트폴리오 일관성 검사
    check_portfolio_consistency()
    
    # 3. 거래 타임라인
    generate_trade_timeline()
    
    print("\n" + "=" * 50)
    print("추가 작업 옵션:")
    print("1. 중복 거래 제거")
    print("2. 포트폴리오 재계산")
    print("3. 종료")
    
    while True:
        choice = input("\n선택하세요 (1-3): ").strip()
        
        if choice == '1':
            clean_duplicate_trades()
        elif choice == '2':
            recalculate_all_portfolios()
        elif choice == '3':
            break
        else:
            print("잘못된 선택입니다.")
    
    print("\n✅ 데이터 검증 완료")

if __name__ == "__main__":
    main()