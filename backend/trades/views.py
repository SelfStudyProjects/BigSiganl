from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Trade
import json
from datetime import datetime

@require_http_methods(["GET", "POST"])
@csrf_exempt
def trade_list_api(request):
    """
    거래 목록 조회 및 생성 API
    """
    if request.method == 'GET':
        # 필터링
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        asset = request.GET.get('asset')
        
        trades = Trade.objects.all().order_by('-timestamp')
        
        if start_date:
            trades = trades.filter(timestamp__gte=start_date)
        if end_date:
            trades = trades.filter(timestamp__lte=end_date)
        if asset:
            trades = trades.filter(asset=asset.upper())
        
        # 페이지네이션
        page = int(request.GET.get('page', 1))
        paginator = Paginator(trades, 20)
        trades_page = paginator.get_page(page)
        
        trades_data = []
        for trade in trades_page:
            trades_data.append({
                'id': trade.id,
                'timestamp': trade.timestamp.isoformat(),
                'asset': trade.asset,
                'action': trade.action,
                'price': float(trade.price),
                'percentage': float(trade.percentage),
                'base_currency': trade.base_currency,
                'created_at': trade.created_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'trades': trades_data,
            'pagination': {
                'current_page': trades_page.number,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': trades_page.has_next(),
                'has_previous': trades_page.has_previous()
            }
        })
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 데이터 검증
            required_fields = ['timestamp', 'asset', 'action', 'price', 'percentage']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'success': False,
                        'error': f'필수 필드 누락: {field}'
                    }, status=400)
            
            # Trade 생성
            trade = Trade.objects.create(
                timestamp=datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00')),
                asset=data['asset'].upper(),
                action=data['action'].upper(),
                price=float(data['price']),
                percentage=float(data['percentage']),
                base_currency=data.get('base_currency', 'KRW'),
                raw_message=data.get('raw_message', '')
            )
            
            return JsonResponse({
                'success': True,
                'trade': {
                    'id': trade.id,
                    'timestamp': trade.timestamp.isoformat(),
                    'asset': trade.asset,
                    'action': trade.action,
                    'price': float(trade.price),
                    'percentage': float(trade.percentage),
                    'base_currency': trade.base_currency
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

def trade_detail_api(request, trade_id):
    """
    개별 거래 상세 조회
    """
    try:
        trade = Trade.objects.get(id=trade_id)
        return JsonResponse({
            'success': True,
            'trade': {
                'id': trade.id,
                'timestamp': trade.timestamp.isoformat(),
                'asset': trade.asset,
                'action': trade.action,
                'price': float(trade.price),
                'percentage': float(trade.percentage),
                'base_currency': trade.base_currency,
                'raw_message': trade.raw_message,
                'created_at': trade.created_at.isoformat()
            }
        })
    except Trade.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': '거래를 찾을 수 없습니다.'
        }, status=404)

def latest_trades_api(request):
    """
    최근 거래 목록
    """
    limit = int(request.GET.get('limit', 20))
    trades = Trade.objects.all().order_by('-timestamp')[:limit]
    
    trades_data = []
    for trade in trades:
        trades_data.append({
            'id': trade.id,
            'timestamp': trade.timestamp.isoformat(),
            'asset': trade.asset,
            'action': trade.action,
            'price': float(trade.price),
            'percentage': float(trade.percentage),
            'base_currency': trade.base_currency
        })
    
    return JsonResponse({
        'success': True,
        'trades': trades_data,
        'count': len(trades_data)
    })