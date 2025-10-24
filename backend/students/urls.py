"""
URL patterns for student endpoints
"""
from django.urls import path
from .views import (
    StudentListCreateView, StudentDetailView, StudentMyProfileView
)

urlpatterns = [
    # Student endpoints
    path('', StudentListCreateView.as_view(), name='student-list-create'),
    path('my-profile/', StudentMyProfileView.as_view(), name='student-my-profile'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
]
