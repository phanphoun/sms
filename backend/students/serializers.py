"""
Serializers for Student Management
"""
from rest_framework import serializers
from .models import Student
from accounts.serializers import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model (read operations)
    """
    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'student_id', 'full_name', 'email',
            'date_of_birth', 'age', 'gender', 'grade',
            'address', 'emergency_contact_name',
            'emergency_contact_phone', 'emergency_contact_relation',
            'enrollment_date', 'gpa', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'enrollment_date', 'created_at', 'updated_at']


class StudentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new student
    """
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Student
        fields = [
            'user_id', 'student_id', 'date_of_birth', 'gender', 'grade',
            'address', 'emergency_contact_name',
            'emergency_contact_phone', 'emergency_contact_relation', 'gpa'
        ]
    
    def validate_student_id(self, value):
        """Validate student ID uniqueness"""
        if Student.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("A student with this ID already exists.")
        return value
    
    def validate_user_id(self, value):
        """Validate that user exists and is a student"""
        from accounts.models import User
        try:
            user = User.objects.get(id=value)
            if user.role != 'STUDENT':
                raise serializers.ValidationError("The specified user is not a student.")
            if hasattr(user, 'student_profile'):
                raise serializers.ValidationError("This user already has a student profile.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        return value


class StudentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating student information
    """
    class Meta:
        model = Student
        fields = [
            'date_of_birth', 'gender', 'grade', 'address',
            'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relation', 'gpa', 'is_active'
        ]
