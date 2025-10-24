"""
Course and Enrollment Management Views
"""
from rest_framework import generics, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .models import Course, Enrollment
from .serializers import (
    CourseSerializer, CourseCreateUpdateSerializer,
    EnrollmentSerializer, EnrollmentCreateSerializer, EnrollmentUpdateSerializer
)
from accounts.permissions import IsAdminOrTeacher, IsAdmin
from accounts.utils import success_response, error_response


class CourseListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list and create courses
    GET /api/courses/
    POST /api/courses/
    """
    queryset = Course.objects.select_related('teacher__user').all()
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['semester', 'academic_year', 'status', 'teacher']
    search_fields = ['course_code', 'course_name', 'teacher__user__first_name', 'teacher__user__last_name']
    ordering_fields = ['created_at', 'course_code']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateUpdateSerializer
        return CourseSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = CourseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CourseSerializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='Courses retrieved successfully'
        )
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Only admins can create courses
        if not request.user.is_admin():
            return error_response(
                message='Only administrators can create courses',
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            course = serializer.save()
            
            return success_response(
                data=CourseSerializer(course).data,
                message='Course created successfully',
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(
                message='Course creation failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to get, update, or delete a specific course
    GET /api/courses/<id>/
    PUT /api/courses/<id>/
    PATCH /api/courses/<id>/
    DELETE /api/courses/<id>/
    """
    queryset = Course.objects.select_related('teacher__user').all()
    permission_classes = [IsAdminOrTeacher]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CourseCreateUpdateSerializer
        return CourseSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CourseSerializer(instance)
        return success_response(
            data=serializer.data,
            message='Course retrieved successfully'
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return success_response(
                data=CourseSerializer(instance).data,
                message='Course updated successfully'
            )
        except Exception as e:
            return error_response(
                message='Course update failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        # Only admins can delete courses
        if not request.user.is_admin():
            return error_response(
                message='Only administrators can delete courses',
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(
            message='Course deleted successfully',
            status_code=status.HTTP_204_NO_CONTENT
        )


class EnrollmentListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list and create enrollments
    GET /api/courses/enrollments/
    POST /api/courses/enrollments/
    """
    queryset = Enrollment.objects.select_related('student__user', 'course__teacher__user').all()
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'course', 'student']
    ordering_fields = ['enrollment_date', 'grade_points']
    ordering = ['-enrollment_date']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EnrollmentCreateSerializer
        return EnrollmentSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = EnrollmentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = EnrollmentSerializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='Enrollments retrieved successfully'
        )
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            
            from students.models import Student
            student = Student.objects.get(id=serializer.validated_data['student_id'])
            course = Course.objects.get(id=serializer.validated_data['course_id'])
            
            enrollment = Enrollment.objects.create(
                student=student,
                course=course
            )
            
            return success_response(
                data=EnrollmentSerializer(enrollment).data,
                message='Enrollment created successfully',
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(
                message='Enrollment creation failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to get, update, or delete a specific enrollment
    GET /api/courses/enrollments/<id>/
    PUT /api/courses/enrollments/<id>/
    PATCH /api/courses/enrollments/<id>/
    DELETE /api/courses/enrollments/<id>/
    """
    queryset = Enrollment.objects.select_related('student__user', 'course__teacher__user').all()
    permission_classes = [IsAdminOrTeacher]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return EnrollmentUpdateSerializer
        return EnrollmentSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EnrollmentSerializer(instance)
        return success_response(
            data=serializer.data,
            message='Enrollment retrieved successfully'
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return success_response(
                data=EnrollmentSerializer(instance).data,
                message='Enrollment updated successfully'
            )
        except Exception as e:
            return error_response(
                message='Enrollment update failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(
            message='Enrollment deleted successfully',
            status_code=status.HTTP_204_NO_CONTENT
        )
