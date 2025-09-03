from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.analysis_dashboard, name='analysis_dashboard'),
]