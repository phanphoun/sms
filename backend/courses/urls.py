"""
URL patterns for course and enrollment endpoints
"""
from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView,
    EnrollmentListCreateView, EnrollmentDetailView
)

urlpatterns = [
    # Course endpoints
    path('', CourseListCreateView.as_view(), name='course-list-create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    
    # Enrollment endpoints
    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
]
