"""
Student Management Views
"""
from rest_framework import generics, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .models import Student
from .serializers import (
    StudentSerializer, StudentCreateSerializer, StudentUpdateSerializer
)
from accounts.permissions import IsAdminOrTeacher, IsAdmin
from accounts.utils import success_response, error_response


class StudentListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list and create students
    GET /api/students/
    POST /api/students/
    """
    queryset = Student.objects.select_related('user').all()
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['grade', 'gender', 'is_active']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['enrollment_date', 'gpa', 'grade']
    ordering = ['-enrollment_date']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudentCreateSerializer
        return StudentSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = StudentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = StudentSerializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='Students retrieved successfully'
        )
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            
            # Get user and create student profile
            from accounts.models import User
            user = User.objects.get(id=serializer.validated_data.pop('user_id'))
            
            student = Student.objects.create(
                user=user,
                **serializer.validated_data
            )
            
            return success_response(
                data=StudentSerializer(student).data,
                message='Student created successfully',
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(
                message='Student creation failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to get, update, or delete a specific student
    GET /api/students/<id>/
    PUT /api/students/<id>/
    PATCH /api/students/<id>/
    DELETE /api/students/<id>/
    """
    queryset = Student.objects.select_related('user').all()
    permission_classes = [IsAdminOrTeacher]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return StudentUpdateSerializer
        return StudentSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StudentSerializer(instance)
        return success_response(
            data=serializer.data,
            message='Student retrieved successfully'
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return success_response(
                data=StudentSerializer(instance).data,
                message='Student updated successfully'
            )
        except Exception as e:
            return error_response(
                message='Student update failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(
            message='Student deleted successfully',
            status_code=status.HTTP_204_NO_CONTENT
        )


class StudentMyProfileView(generics.RetrieveAPIView):
    """
    API endpoint for students to view their own profile
    GET /api/students/my-profile/
    """
    serializer_class = StudentSerializer
    
    def get_object(self):
        # Get the student profile for the current user
        try:
            return Student.objects.select_related('user').get(user=self.request.user)
        except Student.DoesNotExist:
            return None
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return error_response(
                message='Student profile not found',
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message='Your student profile retrieved successfully'
        )
