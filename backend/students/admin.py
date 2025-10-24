"""
Django admin configuration for students app
"""
from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Student model
    """
    list_display = ['student_id', 'full_name', 'email', 'grade', 'gpa', 'is_active', 'enrollment_date']
    list_filter = ['grade', 'gender', 'is_active', 'enrollment_date']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    ordering = ['-enrollment_date']
    date_hierarchy = 'enrollment_date'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Student Information', {
            'fields': ('student_id', 'date_of_birth', 'gender', 'grade')
        }),
        ('Contact Information', {
            'fields': ('address', 'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')
        }),
        ('Academic Information', {
            'fields': ('gpa', 'is_active')
        }),
    )
    
    readonly_fields = ['enrollment_date', 'created_at', 'updated_at']
