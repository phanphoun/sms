"""
Course and Enrollment Models
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from teachers.models import Teacher
from students.models import Student


class Course(models.Model):
    """
    Course model representing subjects/classes
    """
    SEMESTER_CHOICES = [
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Course Information
    course_code = models.CharField(max_length=20, unique=True, db_index=True)
    course_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Teacher Assignment
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses'
    )
    
    # Course Details
    credits = models.PositiveIntegerField(default=3)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    academic_year = models.CharField(max_length=9, help_text="e.g., 2023-2024")
    
    # Schedule
    schedule = models.CharField(max_length=200, help_text="e.g., Mon/Wed/Fri 10:00-11:30")
    room = models.CharField(max_length=50)
    
    # Capacity
    max_students = models.PositiveIntegerField(default=30)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']
        unique_together = [['course_code', 'academic_year', 'semester']]
        indexes = [
            models.Index(fields=['course_code']),
            models.Index(fields=['academic_year', 'semester']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
    @property
    def enrolled_count(self):
        """Get number of enrolled students"""
        return self.enrollments.filter(status='ENROLLED').count()
    
    @property
    def is_full(self):
        """Check if course is at capacity"""
        return self.enrolled_count >= self.max_students


class Enrollment(models.Model):
    """
    Enrollment model representing student course enrollments
    """
    STATUS_CHOICES = [
        ('ENROLLED', 'Enrolled'),
        ('DROPPED', 'Dropped'),
        ('COMPLETED', 'Completed'),
    ]
    
    GRADE_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('F', 'F'),
        ('I', 'Incomplete'),
        ('W', 'Withdrawn'),
    ]
    
    # Primary Key
    id = models.BigAutoField(primary_key=True)
    
    # Relationships
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    
    # Enrollment Details
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ENROLLED')
    
    # Grade Information
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    grade_points = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(4.00)]
    )
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'enrollments'
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        ordering = ['-enrollment_date']
        unique_together = [['student', 'course']]
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['course', 'status']),
            models.Index(fields=['enrollment_date']),
        ]
    
    def __str__(self):
        return f"{self.student.student_id} - {self.course.course_code}"
    
    def save(self, *args, **kwargs):
        """Override save to update grade points based on letter grade"""
        grade_point_map = {
            'A+': 4.00, 'A': 4.00, 'A-': 3.70,
            'B+': 3.30, 'B': 3.00, 'B-': 2.70,
            'C+': 2.30, 'C': 2.00, 'C-': 1.70,
            'D+': 1.30, 'D': 1.00, 'F': 0.00,
            'I': None, 'W': None
        }
        if self.grade:
            self.grade_points = grade_point_map.get(self.grade)
        super().save(*args, **kwargs)
