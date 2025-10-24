"""
Script to create sample courses for testing
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms_backend.settings')
django.setup()

from courses.models import Course
from teachers.models import Teacher
from accounts.models import User

# Create courses
courses_data = [
    {
        'course_code': 'CS101',
        'course_name': 'Introduction to Computer Science',
        'description': 'Fundamentals of computer science including programming, algorithms, and data structures.',
        'credits': 3,
        'semester': '1',
        'academic_year': '2024-2025',
        'status': 'ACTIVE',
        'max_students': 30,
        'schedule': 'Mon/Wed/Fri 10:00-11:30',
        'room': 'CS-101'
    },
    {
        'course_code': 'MATH201',
        'course_name': 'Calculus I',
        'description': 'Introduction to differential and integral calculus.',
        'credits': 4,
        'semester': '1',
        'academic_year': '2024-2025',
        'status': 'ACTIVE',
        'max_students': 25,
        'schedule': 'Tue/Thu 09:00-10:30',
        'room': 'MATH-202'
    },
    {
        'course_code': 'ENG101',
        'course_name': 'English Composition',
        'description': 'Academic writing and critical thinking skills.',
        'credits': 3,
        'semester': '1',
        'academic_year': '2024-2025',
        'status': 'ACTIVE',
        'max_students': 20,
        'schedule': 'Mon/Wed 13:00-14:30',
        'room': 'ENG-101'
    },
    {
        'course_code': 'PHY101',
        'course_name': 'Physics I',
        'description': 'Introduction to mechanics, heat, and sound.',
        'credits': 4,
        'semester': '1',
        'academic_year': '2024-2025',
        'status': 'ACTIVE',
        'max_students': 30,
        'schedule': 'Tue/Thu 14:00-15:30',
        'room': 'PHY-Lab1'
    },
    {
        'course_code': 'CS201',
        'course_name': 'Data Structures',
        'description': 'Advanced data structures and algorithm design.',
        'credits': 3,
        'semester': '2',
        'academic_year': '2024-2025',
        'status': 'ACTIVE',
        'max_students': 25,
        'schedule': 'Mon/Wed/Fri 11:00-12:30',
        'room': 'CS-102'
    }
]

print("=" * 60)
print("Creating Sample Courses")
print("=" * 60)

# Check if we have any teachers, if not create a default one
teachers = Teacher.objects.all()
if not teachers.exists():
    print("\nNo teachers found. Creating a default teacher...")
    # Get or create a teacher user
    teacher_user, created = User.objects.get_or_create(
        email='teacher@example.com',
        defaults={
            'username': 'teacher1',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'TEACHER',
            'is_staff': False
        }
    )
    if created:
        teacher_user.set_password('Teacher123!')
        teacher_user.save()
    
    teacher, created = Teacher.objects.get_or_create(
        user=teacher_user,
        defaults={
            'teacher_id': 'T001',
            'department': 'COMPUTER',
            'qualification': 'Ph.D. in Computer Science',
            'specialization': 'Software Engineering',
            'experience_years': 5
        }
    )
    if created:
        print(f"Created teacher: {teacher.user.full_name}")
    else:
        print(f"Using existing teacher: {teacher.user.full_name}")
else:
    teacher = teachers.first()
    print(f"\nUsing existing teacher: {teacher.user.full_name}")

print("\nCreating courses...")
created_count = 0
updated_count = 0

for course_data in courses_data:
    course_code = course_data['course_code']
    
    # Check if course already exists
    course, created = Course.objects.update_or_create(
        course_code=course_code,
        defaults={
            **course_data,
            'teacher': teacher
        }
    )
    
    if created:
        created_count += 1
        print(f"  [CREATED] {course.course_code} - {course.course_name}")
    else:
        updated_count += 1
        print(f"  [UPDATED] {course.course_code} - {course.course_name}")

print("\n" + "=" * 60)
print(f"Summary:")
print(f"  - Created: {created_count} courses")
print(f"  - Updated: {updated_count} courses")
print(f"  - Total: {Course.objects.count()} courses in database")
print("=" * 60)

# List all courses
print("\nAll Courses:")
for course in Course.objects.all():
    print(f"  - {course.course_code}: {course.course_name} ({course.credits} credits)")
    print(f"    Teacher: {course.teacher.user.full_name}")
    print(f"    Status: {course.status} | Semester: {course.semester} {course.academic_year}")
    print()

print("=" * 60)
print("Done! Courses are ready for testing.")
print("You can now view them at: http://localhost:5173/courses")
print("=" * 60)
