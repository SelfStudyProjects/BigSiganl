from django.urls import path
from . import views

urlpatterns = [
    path('', views.TradeListView.as_view(), name='trade-list'),
    path('<int:pk>/', views.TradeDetailView.as_view(), name='trade-detail'),
    path('latest/', views.LatestTradesView.as_view(), name='trade-latest'),
]