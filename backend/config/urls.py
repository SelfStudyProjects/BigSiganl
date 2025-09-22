# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trades/', include('trades.urls')),
    path('api/portfolios/', include('portfolios.urls')),
    path('api/analysis/', include('analysis.urls')),  # 이 줄이 있는지 확인
]

# 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)