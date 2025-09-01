from django.shortcuts import render
from rest_framework import viewsets
from .models import Portfolio
from .serializers import PortfolioSerializer

class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

def analysis_dashboard(request):
    return render(request, 'analysis/dashboard.html')