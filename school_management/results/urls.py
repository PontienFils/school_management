# results/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/<int:classroom_id>/<int:period_id>/', views.class_results_dashboard, name='class_results_dashboard'),
]