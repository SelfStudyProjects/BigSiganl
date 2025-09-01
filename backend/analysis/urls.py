from django.urls import path
from . import views

urlpatterns = [
    path('portfolio-engine/', views.portfolio_engine, name='portfolio_engine'),
    path('buy-hold-calculator/', views.buy_hold_calculator, name='buy_hold_calculator'),
]