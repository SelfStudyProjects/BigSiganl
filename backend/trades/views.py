from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.filters import OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Trade
from .serializers import TradeSerializer

"""
거래 관련 API 뷰
"""
class TradeListView(ListCreateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['timestamp', 'price']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # 날짜 범위 필터링 (선택사항)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        return queryset
    
    def perform_create(self, serializer):
        # 거래 저장 후 포트폴리오 재계산 트리거 (나중에 구현)
        serializer.save()

class TradeDetailView(RetrieveAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

class LatestTradesView(ListAPIView):
    queryset = Trade.objects.all()[:20]
    serializer_class = TradeSerializer
    ordering = ['-timestamp']