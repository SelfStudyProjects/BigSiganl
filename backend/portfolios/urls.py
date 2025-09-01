from django.urls import path
from . import views

urlpatterns = [
    path('', views.PortfolioListView.as_view(), name='portfolio-list'),
    path('<int:pk>/', views.PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('create/', views.PortfolioCreateView.as_view(), name='portfolio-create'),
    path('update/<int:pk>/', views.PortfolioUpdateView.as_view(), name='portfolio-update'),
    path('delete/<int:pk>/', views.PortfolioDeleteView.as_view(), name='portfolio-delete'),
]