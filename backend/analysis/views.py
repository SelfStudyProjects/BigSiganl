from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, FileResponse, Http404
from django.conf import settings
from pathlib import Path
import os
from datetime import datetime, timedelta

from trades.models import Trade
from portfolios.models import Portfolio, PortfolioSnapshot
from django.db.models import Count, Sum, Avg
from django.utils import timezone

@api_view(['GET'])
def analysis_dashboard(request):
    return Response({'message': 'Analysis Dashboard - 개발 중'})

@api_view(['GET'])
def asset_performance_api(request):
    return Response({'message': 'Asset Performance - 개발 중'})

@api_view(['GET'])
def asset_detail_api(request, asset_name):
    return Response({'message': f'{asset_name} Detail - 개발 중'})

@api_view(['GET'])
def latest_prices_api(request):
    return Response({'message': 'Latest Prices - 개발 중'})

@api_view(['GET'])
def portfolio_vs_assets_comparison(request):
    return Response({'message': 'Portfolio Comparison - 개발 중'})

@api_view(['GET'])
def price_history_summary(request):
    return Response({'message': 'Price History Summary - 개발 중'})

# 새로운 분석 API들
@api_view(['GET'])
def portfolio_performance(request):
    """포트폴리오별 성과 데이터 API"""
    portfolios = Portfolio.objects.all().order_by('-pnl_percentage')
    
    data = []
    for portfolio in portfolios:
        data.append({
            'name': portfolio.name,
            'display_name': portfolio.name.replace('_', ' '),
            'current_value': float(portfolio.current_value),
            'initial_value': float(portfolio.initial_budget),
            'profit_loss': float(portfolio.pnl_absolute),
            'profit_loss_percentage': float(portfolio.profit_loss_percentage),
            'last_updated': portfolio.last_updated
        })
    
    return Response({
        'status': 'success',
        'data': data,
        'meta': {
            'total_portfolios': len(data),
            'timestamp': timezone.now()
        }
    })

@api_view(['GET'])
def dashboard_summary(request):
    """대시보드용 종합 요약 데이터"""
    total_trades = Trade.objects.count()
    total_portfolios = Portfolio.objects.count()
    
    # 최고/최저 성과 포트폴리오
    best_portfolio = Portfolio.objects.order_by('-pnl_percentage').first()
    worst_portfolio = Portfolio.objects.order_by('pnl_percentage').first()
    
    # 총 투자 규모
    total_investment = sum(float(p.initial_budget) for p in Portfolio.objects.all())
    total_current_value = sum(float(p.current_value) for p in Portfolio.objects.all())
    total_profit_loss = total_current_value - total_investment
    total_return_pct = (total_profit_loss / total_investment) * 100 if total_investment > 0 else 0
    
    # 자산별 분포
    asset_distribution = Trade.objects.values('asset').annotate(
        count=Count('id')
    ).order_by('-count')
    
    return Response({
        'status': 'success',
        'data': {
            'overview': {
                'total_trades': total_trades,
                'total_portfolios': total_portfolios,
                'total_investment': total_investment,
                'total_current_value': total_current_value,
                'total_profit_loss': total_profit_loss,
                'total_return_percentage': total_return_pct
            },
            'best_portfolio': {
                'name': best_portfolio.name if best_portfolio else None,
                'display_name': best_portfolio.name.replace('_', ' ') if best_portfolio else None,
                'return_percentage': float(best_portfolio.profit_loss_percentage) if best_portfolio else 0
            },
            'worst_portfolio': {
                'name': worst_portfolio.name if worst_portfolio else None,
                'display_name': worst_portfolio.name.replace('_', ' ') if worst_portfolio else None,
                'return_percentage': float(worst_portfolio.profit_loss_percentage) if worst_portfolio else 0
            },
            'asset_distribution': list(asset_distribution)
        }
    })

# 나머지 뷰들은 기본 구현
@api_view(['GET'])
def portfolio_timeline(request):
    return Response({'message': 'Portfolio Timeline - 개발 중'})

@api_view(['GET'])
def trading_statistics(request):
    return Response({'message': 'Trading Statistics - 개발 중'})

@api_view(['GET'])
def risk_metrics(request):
    return Response({'message': 'Risk Metrics - 개발 중'})

@api_view(['GET'])
def buy_hold_comparison(request):
    return Response({'message': 'Buy Hold Comparison - 개발 중'})

@api_view(['GET'])
def get_chart_image(request, chart_name):
    """생성된 차트 이미지 제공"""
    charts_dir = Path('media') / 'charts'
    chart_file = charts_dir / f'{chart_name}.png'
    
    if not chart_file.exists():
        raise Http404(f"Chart '{chart_name}' not found")
    
    return FileResponse(
        open(chart_file, 'rb'),
        content_type='image/png',
        filename=f'{chart_name}.png'
    )

@api_view(['POST'])
def regenerate_charts(request):
    return Response({'message': 'Regenerate Charts - 개발 중'})

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