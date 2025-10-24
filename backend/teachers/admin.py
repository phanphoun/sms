"""
Django admin configuration for teachers app
"""
from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Teacher model
    """
    list_display = ['teacher_id', 'full_name', 'email', 'department', 'experience_years', 'is_active', 'join_date']
    list_filter = ['department', 'is_active', 'join_date']
    search_fields = ['teacher_id', 'user__first_name', 'user__last_name', 'user__email', 'specialization']
    ordering = ['-join_date']
    date_hierarchy = 'join_date'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Teacher Information', {
            'fields': ('teacher_id', 'department', 'specialization')
        }),
        ('Professional Information', {
            'fields': ('qualification', 'experience_years', 'office_room')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ['join_date', 'created_at', 'updated_at']
