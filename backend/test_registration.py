"""
Test script to verify registration endpoint
"""
import requests
import json

# Test data
test_user = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPass123!",
    "password2": "TestPass123!",
    "first_name": "Test",
    "last_name": "User",
    "phone_number": "1234567890",
    "role": "STUDENT"
}

# API endpoint
url = "http://localhost:8000/api/auth/register/"

print("=" * 60)
print("Testing Registration Endpoint")
print("=" * 60)
print(f"URL: {url}")
print(f"Data: {json.dumps(test_user, indent=2)}")
print("=" * 60)

try:
    response = requests.post(url, json=test_user)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("\n[SUCCESS] Registration successful!")
    else:
        print(f"\n[ERROR] Registration failed with status {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n[ERROR] Could not connect to server!")
    print("Make sure the Django server is running:")
    print("  python manage.py runserver")
    
except Exception as e:
    print(f"\n[ERROR] Unexpected error: {e}")

print("=" * 60)
