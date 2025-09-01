from django.urls import path, include

urlpatterns = [
    path('trades/', include('backend.trades.urls')),
    path('portfolios/', include('backend.portfolios.urls')),
    path('analysis/', include('backend.analysis.urls')),
]