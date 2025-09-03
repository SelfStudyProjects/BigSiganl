from django.urls import path
from . import views

urlpatterns = [
    # 포트폴리오 목록 및 요약
    path('', views.portfolio_list_api, name='portfolio_list_api'),
    path('summary/', views.portfolio_list_api, name='portfolio_summary'),
    
    # 성과 및 비교 데이터
    path('performance/', views.portfolio_performance_api, name='portfolio_performance_api'),
    path('comparison/', views.portfolio_comparison_api, name='portfolio_comparison_api'),
    
    # 개별 포트폴리오 상세
    path('<str:portfolio_name>/', views.portfolio_detail_api, name='portfolio_detail_api'),
    path('<str:portfolio_name>/snapshots/', views.portfolio_snapshots_api, name='portfolio_snapshots_api'),
    
    # 관리 기능
    path('admin/initialize/', views.initialize_portfolios_api, name='initialize_portfolios_api'),
    path('admin/recalculate/', views.recalculate_portfolios_api, name='recalculate_portfolios_api'),
]