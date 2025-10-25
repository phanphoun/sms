import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms_backend.settings')

print("Starting Django setup...")
django.setup()
print("Django setup complete!")

# Try to query database
from django.contrib.auth import get_user_model
User = get_user_model()
print(f"User count: {User.objects.count()}")
print("SUCCESS!")
