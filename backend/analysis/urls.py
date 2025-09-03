from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.analysis_dashboard, name='analysis_dashboard'),
    
    # 자산 성과 관련 API
    path('asset-performance/', views.asset_performance_api, name='asset_performance_api'),
    path('asset/<str:asset_name>/', views.asset_detail_api, name='asset_detail_api'),
    path('latest-prices/', views.latest_prices_api, name='latest_prices_api'),
    
    # 비교 분석 API
    path('comparison/', views.portfolio_vs_assets_comparison, name='portfolio_vs_assets_comparison'),
    
    # 요약 정보 API
    path('summary/', views.price_history_summary, name='price_history_summary'),
]