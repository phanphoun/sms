"""
URL patterns for teacher endpoints
"""
from django.urls import path
from .views import (
    TeacherListCreateView, TeacherDetailView, TeacherMyProfileView
)

urlpatterns = [
    # Teacher endpoints
    path('', TeacherListCreateView.as_view(), name='teacher-list-create'),
    path('my-profile/', TeacherMyProfileView.as_view(), name='teacher-my-profile'),
    path('<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
]
