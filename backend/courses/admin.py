"""
Django admin configuration for courses app
"""
from django.contrib import admin
from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Course model
    """
    list_display = ['course_code', 'course_name', 'teacher', 'semester', 'academic_year', 'enrolled_count', 'max_students', 'status']
    list_filter = ['semester', 'academic_year', 'status', 'teacher']
    search_fields = ['course_code', 'course_name', 'teacher__user__first_name', 'teacher__user__last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('course_code', 'course_name', 'description', 'teacher')
        }),
        ('Course Details', {
            'fields': ('credits', 'semester', 'academic_year', 'schedule', 'room')
        }),
        ('Capacity & Status', {
            'fields': ('max_students', 'status')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Enrollment model
    """
    list_display = ['student', 'course', 'status', 'grade', 'grade_points', 'enrollment_date']
    list_filter = ['status', 'grade', 'enrollment_date']
    search_fields = [
        'student__student_id', 'student__user__first_name', 'student__user__last_name',
        'course__course_code', 'course__course_name'
    ]
    ordering = ['-enrollment_date']
    date_hierarchy = 'enrollment_date'
    
    fieldsets = (
        ('Enrollment Information', {
            'fields': ('student', 'course', 'status')
        }),
        ('Grade Information', {
            'fields': ('grade', 'grade_points')
        }),
    )
    
    readonly_fields = ['enrollment_date', 'updated_at', 'grade_points']
