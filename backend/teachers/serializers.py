"""
Serializers for Teacher Management
"""
from rest_framework import serializers
from .models import Teacher
from accounts.serializers import UserSerializer


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for Teacher model (read operations)
    """
    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    
    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'teacher_id', 'full_name', 'email',
            'department', 'specialization', 'qualification',
            'experience_years', 'join_date', 'office_room',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'join_date', 'created_at', 'updated_at']


class TeacherCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new teacher
    """
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Teacher
        fields = [
            'user_id', 'teacher_id', 'department', 'specialization',
            'qualification', 'experience_years', 'office_room'
        ]
    
    def validate_teacher_id(self, value):
        """Validate teacher ID uniqueness"""
        if Teacher.objects.filter(teacher_id=value).exists():
            raise serializers.ValidationError("A teacher with this ID already exists.")
        return value
    
    def validate_user_id(self, value):
        """Validate that user exists and is a teacher"""
        from accounts.models import User
        try:
            user = User.objects.get(id=value)
            if user.role != 'TEACHER':
                raise serializers.ValidationError("The specified user is not a teacher.")
            if hasattr(user, 'teacher_profile'):
                raise serializers.ValidationError("This user already has a teacher profile.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        return value


class TeacherUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating teacher information
    """
    class Meta:
        model = Teacher
        fields = [
            'department', 'specialization', 'qualification',
            'experience_years', 'office_room', 'is_active'
        ]
