from django.shortcuts import render
from django.http import JsonResponse
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
from .models import Portfolio, PortfolioSnapshot
from analysis.portfolio_engine import PortfolioEngine, initialize_system, recalculate_system
import logging

logger = logging.getLogger(__name__)

# class PortfolioViewSet(viewsets.ModelViewSet):
#     """
#     포트폴리오 관련 API ViewSet (DRF 없이 간단하게)
#     """
#     queryset = Portfolio.objects.filter(is_active=True)

def portfolio_list_api(request):
    """
    모든 포트폴리오 목록 및 현재 상태 반환
    """
    engine = PortfolioEngine()
    portfolios_summary = engine.get_all_portfolios_summary()
    
    return JsonResponse({
        'success': True,
        'portfolios': portfolios_summary,
        'count': len(portfolios_summary)
    })

def portfolio_detail_api(request, portfolio_name):
    """
    특정 포트폴리오 상세 정보
    """
    try:
        portfolio = Portfolio.objects.get(name=portfolio_name, is_active=True)
    except Portfolio.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'포트폴리오를 찾을 수 없습니다: {portfolio_name}'
        }, status=404)
    
    # 성과 데이터
    days = int(request.GET.get('days', 30))
    engine = PortfolioEngine()
    performance_data = engine.get_portfolio_performance_data(portfolio_name, days)
    
    # 자산 배분 계산
    total_value = float(portfolio.current_value)
    asset_allocation = {}
    
    if total_value > 0:
        # 현금 비율
        asset_allocation['CASH'] = float(portfolio.cash_balance) / total_value * 100
        
        # 각 자산 비율
        current_prices = engine.get_current_prices(portfolio.last_updated)
        for asset, quantity in portfolio.holdings.items():
            if float(quantity) > 0:
                asset_value = float(quantity) * float(current_prices.get(asset, 0))
                asset_allocation[asset] = asset_value / total_value * 100
    
    return JsonResponse({
        'success': True,
        'portfolio': {
            'name': portfolio.name,
            'description': portfolio.description,
            'assets': portfolio.assets,
            'current_value': float(portfolio.current_value),
            'pnl_absolute': float(portfolio.pnl_absolute),
            'pnl_percentage': float(portfolio.pnl_percentage),
            'cash_balance': float(portfolio.cash_balance),
            'holdings': {k: float(v) for k, v in portfolio.holdings.items()},
            'asset_allocation': asset_allocation,
            'last_updated': portfolio.last_updated.isoformat()
        },
        'performance_data': performance_data,
        'period_days': days
    })

def portfolio_performance_api(request):
    """
    모든 포트폴리오의 성과 비교 데이터 (차트용)
    """
    days = int(request.GET.get('days', 30))
    selected_portfolios = request.GET.get('portfolios', '').split(',')
    
    if not selected_portfolios or selected_portfolios == ['']:
        # 선택된 포트폴리오가 없으면 모두 포함
        portfolios = Portfolio.objects.filter(is_active=True)
        selected_portfolios = [p.name for p in portfolios]
    
    engine = PortfolioEngine()
    chart_data = {}
    
    for portfolio_name in selected_portfolios:
        if portfolio_name.strip():
            performance_data = engine.get_portfolio_performance_data(portfolio_name.strip(), days)
            if performance_data:
                chart_data[portfolio_name.strip()] = {
                    'name': portfolio_name.strip(),
                    'type': 'portfolio',
                    'data': performance_data
                }
    
    return JsonResponse({
        'success': True,
        'chart_data': chart_data,
        'period_days': days
    })

def portfolio_comparison_api(request):
    """
    포트폴리오 성과 비교 테이블용 데이터
    """
    portfolios = Portfolio.objects.filter(is_active=True).order_by('name')
    
    comparison_data = []
    for portfolio in portfolios:
        # 최신 스냅샷에서 최대 보유 자산 찾기
        max_asset = 'CASH'
        max_value = float(portfolio.cash_balance)
        
        current_prices = PortfolioEngine().get_current_prices(portfolio.last_updated)
        for asset, quantity in portfolio.holdings.items():
            if float(quantity) > 0:
                asset_value = float(quantity) * float(current_prices.get(asset, 0))
                if asset_value > max_value:
                    max_value = asset_value
                    max_asset = asset
        
        comparison_data.append({
            'name': portfolio.name,
            'current_value': float(portfolio.current_value),
            'pnl_absolute': float(portfolio.pnl_absolute),
            'pnl_percentage': float(portfolio.pnl_percentage),
            'max_asset': max_asset,
            'max_asset_value': max_value,
            'cash_ratio': float(portfolio.cash_balance) / float(portfolio.current_value) * 100 if portfolio.current_value > 0 else 0
        })
    
    return JsonResponse({
        'success': True,
        'comparison_data': comparison_data
    })

def initialize_portfolios_api(request):
    """
    포트폴리오 초기화 API (관리자용)
    """
    if request.method in ['POST', 'GET']:
        try:
            portfolios = initialize_system()
            return JsonResponse({
                'success': True,
                'message': f'{portfolios.count()}개 포트폴리오가 초기화되었습니다.',
                'portfolios': [p.name for p in portfolios]
            })
        except Exception as e:
            logger.error(f"포트폴리오 초기화 실패: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'POST 또는 GET 요청만 허용됩니다.'
    }, status=405)

def recalculate_portfolios_api(request):
    """
    전체 포트폴리오 재계산 API (관리자용)
    """
    if request.method in ['POST', 'GET']:
        try:
            recalculate_system()
            return JsonResponse({
                'success': True,
                'message': '모든 포트폴리오가 재계산되었습니다.'
            })
        except Exception as e:
            logger.error(f"포트폴리오 재계산 실패: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'POST 또는 GET 요청만 허용됩니다.'
    }, status=405)

def portfolio_snapshots_api(request, portfolio_name):
    """
    특정 포트폴리오의 스냅샷 이력
    """
    try:
        portfolio = Portfolio.objects.get(name=portfolio_name, is_active=True)
    except Portfolio.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'포트폴리오를 찾을 수 없습니다: {portfolio_name}'
        }, status=404)
    
    limit = int(request.GET.get('limit', 100))
    snapshots = portfolio.snapshots.all()[:limit]
    
    snapshot_data = []
    for snapshot in snapshots:
        snapshot_data.append({
            'timestamp': snapshot.timestamp.isoformat(),
            'portfolio_value': float(snapshot.portfolio_value),
            'pnl_percentage': float(snapshot.pnl_percentage),
            'cash_balance': float(snapshot.cash_balance),
            'holdings': snapshot.holdings,
            'triggered_by_trade': snapshot.trade_triggered_by.id if snapshot.trade_triggered_by else None
        })
    
    return JsonResponse({
        'success': True,
        'portfolio_name': portfolio_name,
        'snapshots': snapshot_data,
        'total_count': portfolio.snapshots.count()
    })