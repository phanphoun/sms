"""
Teacher Model and Related Information
"""
from django.db import models
from django.conf import settings


class Teacher(models.Model):
    """
    Teacher model extending the User model
    """
    DEPARTMENT_CHOICES = [
        ('MATH', 'Mathematics'),
        ('SCIENCE', 'Science'),
        ('ENGLISH', 'English'),
        ('HISTORY', 'History'),
        ('GEOGRAPHY', 'Geography'),
        ('PHYSICS', 'Physics'),
        ('CHEMISTRY', 'Chemistry'),
        ('BIOLOGY', 'Biology'),
        ('COMPUTER', 'Computer Science'),
        ('ART', 'Art'),
        ('MUSIC', 'Music'),
        ('PE', 'Physical Education'),
        ('OTHER', 'Other'),
    ]
    
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Link to User model (One-to-One)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    
    # Teacher Information
    teacher_id = models.CharField(max_length=20, unique=True, db_index=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    specialization = models.CharField(max_length=100)
    
    # Professional Information
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(default=0)
    join_date = models.DateField(auto_now_add=True)
    
    # Contact & Additional Info
    office_room = models.CharField(max_length=50, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teachers'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        ordering = ['-join_date']
        indexes = [
            models.Index(fields=['teacher_id']),
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        return f"{self.teacher_id} - {self.user.full_name}"
    
    @property
    def full_name(self):
        """Return teacher's full name from user"""
        return self.user.full_name
    
    @property
    def email(self):
        """Return teacher's email from user"""
        return self.user.email
