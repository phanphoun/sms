"""
Serializers for Course and Enrollment Management
"""
from rest_framework import serializers
from .models import Course, Enrollment
from teachers.serializers import TeacherSerializer
from students.serializers import StudentSerializer


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model (read operations)
    """
    teacher = TeacherSerializer(read_only=True)
    enrolled_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'course_code', 'course_name', 'description',
            'teacher', 'credits', 'semester', 'academic_year',
            'schedule', 'room', 'max_students', 'enrolled_count',
            'is_full', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating courses
    """
    teacher_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Course
        fields = [
            'course_code', 'course_name', 'description', 'teacher_id',
            'credits', 'semester', 'academic_year', 'schedule',
            'room', 'max_students', 'status'
        ]
    
    def validate_teacher_id(self, value):
        """Validate that teacher exists"""
        if value is not None:
            from teachers.models import Teacher
            if not Teacher.objects.filter(id=value).exists():
                raise serializers.ValidationError("Teacher does not exist.")
        return value
    
    def create(self, validated_data):
        teacher_id = validated_data.pop('teacher_id', None)
        if teacher_id:
            from teachers.models import Teacher
            validated_data['teacher'] = Teacher.objects.get(id=teacher_id)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        teacher_id = validated_data.pop('teacher_id', None)
        if teacher_id is not None:
            from teachers.models import Teacher
            instance.teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None
        return super().update(instance, validated_data)


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Enrollment model (read operations)
    """
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'enrollment_date',
            'status', 'grade', 'grade_points', 'updated_at'
        ]
        read_only_fields = ['id', 'enrollment_date', 'updated_at', 'grade_points']


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating enrollments
    """
    student_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    
    class Meta:
        model = Enrollment
        fields = ['student_id', 'course_id']
    
    def validate(self, attrs):
        """Validate enrollment creation"""
        from students.models import Student
        
        # Check if student exists
        try:
            student = Student.objects.get(id=attrs['student_id'])
        except Student.DoesNotExist:
            raise serializers.ValidationError({"student_id": "Student does not exist."})
        
        # Check if course exists
        try:
            course = Course.objects.get(id=attrs['course_id'])
        except Course.DoesNotExist:
            raise serializers.ValidationError({"course_id": "Course does not exist."})
        
        # Check if course is active
        if course.status != 'ACTIVE':
            raise serializers.ValidationError({"course_id": "Course is not active."})
        
        # Check if course is full
        if course.is_full:
            raise serializers.ValidationError({"course_id": "Course is full."})
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Student is already enrolled in this course.")
        
        return attrs


class EnrollmentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating enrollment status and grades
    """
    class Meta:
        model = Enrollment
        fields = ['status', 'grade']
