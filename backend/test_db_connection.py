import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms_backend.settings')
django.setup()

from django.db import connection
from django.db.utils import OperationalError

try:
    # Test connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE(), USER(), VERSION()")
        result = cursor.fetchone()
        
    print("=" * 60)
    print("[SUCCESS] DATABASE CONNECTION SUCCESSFUL!")
    print("=" * 60)
    print(f"Database: {result[0]}")
    print(f"User: {result[1]}")
    print(f"Server Version: {result[2]}")
    print("=" * 60)
    
    # Show tables
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
    
    if tables:
        print(f"\n[INFO] Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("\n[WARNING] No tables found (database is empty)")
        print("Run 'python manage.py migrate' to create tables")
    
    print("=" * 60)
    
except OperationalError as e:
    print("=" * 60)
    print("[ERROR] DATABASE CONNECTION FAILED!")
    print("=" * 60)
    print(f"Error: {e}")
    print("\nCheck your .env file:")
    print("  - DB_NAME")
    print("  - DB_USER")
    print("  - DB_PASSWORD")
    print("  - DB_HOST")
    print("  - DB_PORT")
    print("=" * 60)
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
    sys.exit(1)
