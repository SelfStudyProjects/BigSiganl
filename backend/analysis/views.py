from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from trades.models import Trade, PriceHistory
from .price_tracker import PriceTracker, get_asset_chart_data

def analysis_dashboard(request):
    """기본 대시보드 템플릿"""
    return render(request, 'analysis/dashboard.html')

def asset_performance_api(request):
    """
    개별 자산들의 성과 데이터 API
    BTC, USDT, DOGE, USDC 각각의 가격 변동률 제공
    """
    days = int(request.GET.get('days', 30))
    
    tracker = PriceTracker()
    asset_data = {}
    
    # 각 자산별 성과 데이터 수집
    for asset in settings.SUPPORTED_ASSETS + ['USDC']:
        performance_data = tracker.get_asset_performance_data(asset, days)
        
        if performance_data:
            asset_data[asset] = {
                'name': asset,
                'performance_history': performance_data,
                'latest_price': performance_data[-1]['price'] if performance_data else 0,
                'total_return': performance_data[-1]['return_percentage'] if performance_data else 0,
                'latest_change': performance_data[-1]['price_change_percentage'] if performance_data else 0
            }
        else:
            # 데이터가 없는 경우 기본값
            asset_data[asset] = {
                'name': asset,
                'performance_history': [],
                'latest_price': 0,
                'total_return': 0,
                'latest_change': 0
            }
    
    return JsonResponse({
        'success': True,
        'data': asset_data,
        'period_days': days,
        'last_updated': tracker.get_latest_prices()
    })

def latest_prices_api(request):
    """
    모든 자산의 최신 가격 정보 API
    """
    tracker = PriceTracker()
    latest_prices = tracker.get_latest_prices()
    
    return JsonResponse({
        'success': True,
        'prices': latest_prices
    })

def asset_detail_api(request, asset_name):
    """
    특정 자산의 상세 성과 데이터
    """
    asset_name = asset_name.upper()
    days = int(request.GET.get('days', 30))
    
    if asset_name not in (settings.SUPPORTED_ASSETS + ['USDC']):
        return JsonResponse({
            'success': False,
            'error': f'지원하지 않는 자산: {asset_name}'
        }, status=400)
    
    performance_data = get_asset_chart_data(asset_name, days)
    
    # 통계 계산
    if performance_data:
        returns = [item['return_percentage'] for item in performance_data]
        max_return = max(returns)
        min_return = min(returns)
        volatility = calculate_volatility(returns)
        
        stats = {
            'max_return': max_return,
            'min_return': min_return,
            'volatility': volatility,
            'total_trades': len(performance_data)
        }
    else:
        stats = {
            'max_return': 0,
            'min_return': 0,
            'volatility': 0,
            'total_trades': 0
        }
    
    return JsonResponse({
        'success': True,
        'asset': asset_name,
        'performance_data': performance_data,
        'statistics': stats
    })

def portfolio_vs_assets_comparison(request):
    """
    포트폴리오 성과 vs 개별 자산 성과 비교 API
    """
    days = int(request.GET.get('days', 30))
    
    # 개별 자산 성과 데이터
    tracker = PriceTracker()
    asset_performance = {}
    
    for asset in settings.SUPPORTED_ASSETS + ['USDC']:
        performance_data = tracker.get_asset_performance_data(asset, days)
        if performance_data:
            asset_performance[f'{asset}_Individual'] = {
                'name': f'{asset} (개별 보유)',
                'type': 'individual_asset',
                'data': performance_data
            }
    
    # TODO: 포트폴리오 성과 데이터 추가 (portfolio_engine.py 완성 후)
    portfolio_performance = {
        'BTC_Only': {'name': 'BTC 전용 포트폴리오', 'type': 'portfolio', 'data': []},
        'Multi_Asset': {'name': '다중 자산 포트폴리오', 'type': 'portfolio', 'data': []}
    }
    
    return JsonResponse({
        'success': True,
        'comparison_data': {
            'individual_assets': asset_performance,
            'portfolios': portfolio_performance
        }
    })

def price_history_summary(request):
    """
    전체 가격 이력 요약 정보
    """
    summary = {}
    
    for asset in settings.SUPPORTED_ASSETS + ['USDC']:
        trade_count = Trade.objects.filter(asset=asset).count()
        price_history_count = PriceHistory.objects.filter(asset=asset).count()
        
        latest_trade = Trade.objects.filter(asset=asset).first()
        latest_price_record = PriceHistory.objects.filter(asset=asset).first()
        
        summary[asset] = {
            'total_trades': trade_count,
            'price_records': price_history_count,
            'latest_trade_time': latest_trade.timestamp.isoformat() if latest_trade else None,
            'latest_price_time': latest_price_record.timestamp.isoformat() if latest_price_record else None,
            'has_price_data': price_history_count > 0
        }
    
    return JsonResponse({
        'success': True,
        'summary': summary
    })

# 헬퍼 함수
def calculate_volatility(returns):
    """수익률 리스트에서 변동성 계산"""
    if len(returns) < 2:
        return 0
    
    mean_return = sum(returns) / len(returns)
    squared_diffs = [(r - mean_return) ** 2 for r in returns]
    variance = sum(squared_diffs) / (len(squared_diffs) - 1)
    volatility = variance ** 0.5
    
    return round(volatility, 4)