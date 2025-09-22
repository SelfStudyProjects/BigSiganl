# analysis/urls.py
from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    # 기존 URL들 (호환성 유지)
    path('dashboard/', views.analysis_dashboard, name='analysis_dashboard'),
    path('asset-performance/', views.asset_performance_api, name='asset_performance_api'),
    path('asset/<str:asset_name>/', views.asset_detail_api, name='asset_detail_api'),
    path('latest-prices/', views.latest_prices_api, name='latest_prices_api'),
    path('comparison/', views.portfolio_vs_assets_comparison, name='portfolio_vs_assets_comparison'),
    path('summary/', views.price_history_summary, name='price_history_summary'),
    
    # 새로운 분석 API들
    path('performance/', views.portfolio_performance, name='portfolio_performance'),
    path('timeline/', views.portfolio_timeline, name='portfolio_timeline'),
    path('trading-stats/', views.trading_statistics, name='trading_statistics'),
    path('risk-metrics/', views.risk_metrics, name='risk_metrics'),
    path('buy-hold-comparison/', views.buy_hold_comparison, name='buy_hold_comparison'),
    path('dashboard-summary/', views.dashboard_summary, name='dashboard_summary'),
    path('charts/<str:chart_name>/', views.get_chart_image, name='get_chart_image'),
    path('regenerate-charts/', views.regenerate_charts, name='regenerate_charts'),
]