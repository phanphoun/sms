"""
Teacher Management Views
"""
from rest_framework import generics, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .models import Teacher
from .serializers import (
    TeacherSerializer, TeacherCreateSerializer, TeacherUpdateSerializer
)
from accounts.permissions import IsAdminOrTeacher, IsAdmin
from accounts.utils import success_response, error_response


class TeacherListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list and create teachers
    GET /api/teachers/
    POST /api/teachers/
    """
    queryset = Teacher.objects.select_related('user').all()
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'is_active']
    search_fields = ['teacher_id', 'user__first_name', 'user__last_name', 'user__email', 'specialization']
    ordering_fields = ['join_date', 'experience_years']
    ordering = ['-join_date']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TeacherCreateSerializer
        return TeacherSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = TeacherSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TeacherSerializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='Teachers retrieved successfully'
        )
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Only admins can create teachers
        if not request.user.is_admin():
            return error_response(
                message='Only administrators can create teacher profiles',
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            
            # Get user and create teacher profile
            from accounts.models import User
            user = User.objects.get(id=serializer.validated_data.pop('user_id'))
            
            teacher = Teacher.objects.create(
                user=user,
                **serializer.validated_data
            )
            
            return success_response(
                data=TeacherSerializer(teacher).data,
                message='Teacher created successfully',
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(
                message='Teacher creation failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to get, update, or delete a specific teacher
    GET /api/teachers/<id>/
    PUT /api/teachers/<id>/
    PATCH /api/teachers/<id>/
    DELETE /api/teachers/<id>/
    """
    queryset = Teacher.objects.select_related('user').all()
    permission_classes = [IsAdminOrTeacher]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TeacherUpdateSerializer
        return TeacherSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TeacherSerializer(instance)
        return success_response(
            data=serializer.data,
            message='Teacher retrieved successfully'
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return success_response(
                data=TeacherSerializer(instance).data,
                message='Teacher updated successfully'
            )
        except Exception as e:
            return error_response(
                message='Teacher update failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        # Only admins can delete teachers
        if not request.user.is_admin():
            return error_response(
                message='Only administrators can delete teacher profiles',
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(
            message='Teacher deleted successfully',
            status_code=status.HTTP_204_NO_CONTENT
        )


class TeacherMyProfileView(generics.RetrieveAPIView):
    """
    API endpoint for teachers to view their own profile
    GET /api/teachers/my-profile/
    """
    serializer_class = TeacherSerializer
    
    def get_object(self):
        # Get the teacher profile for the current user
        try:
            return Teacher.objects.select_related('user').get(user=self.request.user)
        except Teacher.DoesNotExist:
            return None
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return error_response(
                message='Teacher profile not found',
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message='Your teacher profile retrieved successfully'
        )
