"""
Authentication and User Management Views
"""
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.db import transaction

from .models import User
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    ChangePasswordSerializer, UserUpdateSerializer
)
from .permissions import IsAdmin, IsOwnerOrAdmin
from .utils import success_response, error_response


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return success_response(
                data={
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                },
                message='User registered successfully',
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(
                message='Registration failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class LoginView(views.APIView):
    """
    API endpoint for user login
    POST /api/auth/login/
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            
            if user is None:
                return error_response(
                    message='Invalid credentials',
                    details={'email': 'Email or password is incorrect'},
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            
            if not user.is_active:
                return error_response(
                    message='Account is inactive',
                    details={'email': 'This account has been deactivated'},
                    status_code=status.HTTP_403_FORBIDDEN
                )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return success_response(
                data={
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                },
                message='Login successful'
            )
            
        except Exception as e:
            return error_response(
                message='Login failed',
                details=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(views.APIView):
    """
    API endpoint for user logout (blacklist refresh token)
    POST /api/auth/logout/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return error_response(
                    message='Refresh token is required',
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return success_response(
                message='Logout successful'
            )
        except Exception as e:
            return error_response(
                message='Logout failed',
                details=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get and update user profile
    GET /api/auth/profile/
    PUT /api/auth/profile/
    PATCH /api/auth/profile/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user)
        return success_response(
            data=serializer.data,
            message='Profile retrieved successfully'
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return success_response(
                data=UserSerializer(instance).data,
                message='Profile updated successfully'
            )
        except Exception as e:
            return error_response(
                message='Profile update failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(views.APIView):
    """
    API endpoint for changing password
    POST /api/auth/change-password/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        try:
            serializer.is_valid(raise_exception=True)
            
            # Set new password
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return success_response(
                message='Password changed successfully'
            )
        except Exception as e:
            return error_response(
                message='Password change failed',
                details=serializer.errors if hasattr(serializer, 'errors') else str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class UserListView(generics.ListAPIView):
    """
    API endpoint to list all users (Admin only)
    GET /api/auth/users/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='Users retrieved successfully'
        )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to get, update, or delete a specific user (Admin only)
    GET /api/auth/users/<id>/
    PUT /api/auth/users/<id>/
    PATCH /api/auth/users/<id>/
    DELETE /api/auth/users/<id>/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message='User retrieved successfully'
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(
            message='User deleted successfully',
            status_code=status.HTTP_204_NO_CONTENT
        )
