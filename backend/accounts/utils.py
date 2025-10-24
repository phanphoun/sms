"""
Utility functions for accounts app
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the response format
        custom_response_data = {
            'success': False,
            'error': {
                'message': 'An error occurred',
                'details': response.data
            }
        }
        
        # Extract error message
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['error']['message'] = response.data['detail']
            elif 'non_field_errors' in response.data:
                custom_response_data['error']['message'] = response.data['non_field_errors'][0]
            else:
                # Get first error message
                first_key = list(response.data.keys())[0]
                if isinstance(response.data[first_key], list):
                    custom_response_data['error']['message'] = response.data[first_key][0]
                else:
                    custom_response_data['error']['message'] = str(response.data[first_key])
        elif isinstance(response.data, list):
            custom_response_data['error']['message'] = response.data[0]
        else:
            custom_response_data['error']['message'] = str(response.data)
        
        response.data = custom_response_data
    
    # Handle Django validation errors
    elif isinstance(exc, DjangoValidationError):
        response = Response(
            {
                'success': False,
                'error': {
                    'message': 'Validation error',
                    'details': exc.message_dict if hasattr(exc, 'message_dict') else {'detail': exc.messages}
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Handle unexpected errors
    else:
        response = Response(
            {
                'success': False,
                'error': {
                    'message': 'An unexpected error occurred',
                    'details': str(exc)
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response


def success_response(data=None, message='Success', status_code=status.HTTP_200_OK):
    """
    Generate a standardized success response
    """
    response_data = {
        'success': True,
        'message': message,
    }
    if data is not None:
        response_data['data'] = data
    
    return Response(response_data, status=status_code)


def error_response(message='Error', details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Generate a standardized error response
    """
    response_data = {
        'success': False,
        'error': {
            'message': message,
        }
    }
    if details is not None:
        response_data['error']['details'] = details
    
    return Response(response_data, status=status_code)
