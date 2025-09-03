from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trades/', include('trades.urls')),
    path('api/portfolios/', include('portfolios.urls')),
    path('api/analysis/', include('analysis.urls')),
]