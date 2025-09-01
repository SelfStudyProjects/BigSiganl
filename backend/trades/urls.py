from django.urls import path
from . import views

urlpatterns = [
    path('', views.TradeListView.as_view(), name='trade-list'),
    path('<int:pk>/', views.TradeDetailView.as_view(), name='trade-detail'),
    path('create/', views.TradeCreateView.as_view(), name='trade-create'),
    path('update/<int:pk>/', views.TradeUpdateView.as_view(), name='trade-update'),
    path('delete/<int:pk>/', views.TradeDeleteView.as_view(), name='trade-delete'),
]