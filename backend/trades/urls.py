from django.urls import path
from . import views

urlpatterns = [
    path('', views.trade_list_api, name='trade_list_api'),
    path('<int:trade_id>/', views.trade_detail_api, name='trade_detail_api'),
    path('latest/', views.latest_trades_api, name='latest_trades_api'),
]