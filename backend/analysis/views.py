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
from django.db.models import Count, Sum, Avg
from django.utils import timezone

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