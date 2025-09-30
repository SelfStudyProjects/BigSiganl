from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, FileResponse, Http404
from django.shortcuts import render  # 추가
from django.conf import settings
from pathlib import Path
import os
from datetime import datetime, timedelta
from trades.models import Trade
from portfolios.models import Portfolio, PortfolioSnapshot
from django.db.models import Count, Sum, Avg, F, Value, DecimalField, ExpressionWrapper
from django.utils import timezone
from django.shortcuts import render

@api_view(['GET'])
def analysis_dashboard(request):
    """분석 대시보드 페이지 (기존 호환성 유지)"""
    return render(request, 'analysis/dashboard.html')

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
            'total_return': float(portfolio.pnl_percentage),  # 수정: profit_loss_percentage → pnl_percentage
            'final_value': float(portfolio.current_value),
            'initial_value': float(portfolio.initial_budget),
            'profit_loss': float(portfolio.pnl_absolute),
        })
    
    return Response({
        'status': 'success',
        'portfolios': data,  # 수정: data → portfolios
        'total_portfolios': len(data),
        'timestamp': timezone.now()
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
            'return_percentage': float(best_portfolio.pnl_percentage) if best_portfolio else 0
        },
        'worst_portfolio': {
            'name': worst_portfolio.name if worst_portfolio else None,
            'display_name': worst_portfolio.name.replace('_', ' ') if worst_portfolio else None,
            'return_percentage': float(worst_portfolio.pnl_percentage) if worst_portfolio else 0
        },
        'asset_distribution': list(asset_distribution)
    })

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

# 개발 중인 API들 (플레이스홀더)
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

@api_view(['POST'])
def regenerate_charts(request):
    return Response({'message': 'Regenerate Charts - 개발 중'})

@api_view(['GET'])
def asset_performance_api(request):
    """자산별 성과 API (기존 호환성)"""
    return Response({'message': 'Asset Performance API - 개발 중'})

@api_view(['GET'])
def asset_detail_api(request, asset_name):
    """특정 자산 상세 정보"""
    return Response({
        'asset': asset_name,
        'message': 'Asset Detail API - 개발 중'
    })

@api_view(['GET'])
def latest_prices_api(request):
    """최신 가격 정보"""
    return Response({'message': 'Latest Prices API - 개발 중'})

@api_view(['GET'])
def portfolio_vs_assets_comparison(request):
    """포트폴리오 vs 자산 비교"""
    return Response({'message': 'Portfolio vs Assets Comparison - 개발 중'})

@api_view(['GET'])
def price_history_summary(request):
    """가격 히스토리 요약"""
    return Response({'message': 'Price History Summary - 개발 중'})

@api_view(['GET'])
def portfolio_timeline(request):
    """시간별 포트폴리오 가치 변화"""
    portfolio_name = request.GET.get('portfolio', 'All_Assets')
    days = int(request.GET.get('days', 30))
    
    try:
        portfolio = Portfolio.objects.get(name=portfolio_name)
        snapshots = list(PortfolioSnapshot.objects.filter(
            portfolio=portfolio
        ).order_by('-timestamp')[:days*24])  # 시간별 데이터

        timeline_data = [{
            'timestamp': snap.timestamp.isoformat(),
            'value': float(snap.portfolio_value),
            'pnl': float(snap.pnl_percentage)
        } for snap in reversed(snapshots)]
        
        return Response({
            'status': 'success',
            'portfolio': portfolio_name,
            'timeline': timeline_data
        })
    except Portfolio.DoesNotExist:
        return Response({'error': 'Portfolio not found'}, status=404)

@api_view(['GET'])
def trading_statistics(request):
    """거래 통계 분석"""
    trades = Trade.objects.all()
    
    total_trades = trades.count()
    buy_count = trades.filter(action='BUY').count()
    sell_count = trades.filter(action='SELL').count()
    
    # 자산별 통계
    # Trade에는 `amount` 필드가 없으므로, 단순화하여 거래별 명목(notional) 금액 = price * (percentage / 100) 합계를 계산합니다.
    notional_expr = ExpressionWrapper(
        F('price') * (F('percentage') / Value(100)),
        output_field=DecimalField(max_digits=20, decimal_places=2)
    )
    asset_stats = trades.values('asset').annotate(
        count=Count('id'),
        total_notional=Sum(notional_expr)
    ).order_by('-count')
    
    return Response({
        'status': 'success',
        'overview': {
            'total_trades': total_trades,
            'buy_trades': buy_count,
            'sell_trades': sell_count,
            'buy_ratio': round(buy_count/total_trades*100, 2) if total_trades > 0 else 0
        },
        'asset_breakdown': list(asset_stats)
    })

@api_view(['GET'])
def risk_metrics(request):
    """리스크 메트릭 계산"""
    portfolios = Portfolio.objects.all()
    
    risk_data = []
    for portfolio in portfolios:
        snapshots = list(PortfolioSnapshot.objects.filter(
            portfolio=portfolio
        ).order_by('timestamp'))

        if len(snapshots) < 2:
            continue

        returns = []
        for i in range(1, len(snapshots)):
            prev_val = float(snapshots[i-1].portfolio_value)
            curr_val = float(snapshots[i].portfolio_value)
            if prev_val > 0:
                returns.append((curr_val - prev_val) / prev_val)
        
        if returns:
            import numpy as np
            volatility = np.std(returns) * np.sqrt(365) * 100  # 연율화
            max_return = max(returns) * 100
            min_return = min(returns) * 100
        else:
            volatility = 0
            max_return = 0
            min_return = 0
        
        risk_data.append({
            'name': portfolio.name,
            'display_name': portfolio.name.replace('_', ' '),
            'volatility': round(volatility, 2),
            'max_daily_return': round(max_return, 2),
            'min_daily_return': round(min_return, 2),
            'current_return': float(portfolio.pnl_percentage)
        })
    
    return Response({
        'status': 'success',
        'risk_metrics': risk_data
    })