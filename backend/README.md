# Backend - Student Management System

Django REST Framework backend with JWT authentication.

## Quick Start

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Setup environment:
```bash
copy .env.example .env
# Edit .env with your database credentials
```

4. Create database:
```sql
CREATE DATABASE sms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run server:
```bash
python manage.py runserver
```

## API Documentation

### Authentication
- **POST** `/api/auth/register/` - Register new user
- **POST** `/api/auth/login/` - Login
- **POST** `/api/auth/logout/` - Logout
- **POST** `/api/auth/token/refresh/` - Refresh token
- **GET** `/api/auth/profile/` - Get profile
- **PUT** `/api/auth/profile/` - Update profile
- **POST** `/api/auth/change-password/` - Change password

### Students (Admin/Teacher)
- **GET** `/api/students/` - List students
- **POST** `/api/students/` - Create student
- **GET** `/api/students/{id}/` - Get student
- **PUT** `/api/students/{id}/` - Update student
- **DELETE** `/api/students/{id}/` - Delete student

### Teachers (Admin/Teacher)
- **GET** `/api/teachers/` - List teachers
- **POST** `/api/teachers/` - Create teacher (Admin only)
- **GET** `/api/teachers/{id}/` - Get teacher
- **PUT** `/api/teachers/{id}/` - Update teacher
- **DELETE** `/api/teachers/{id}/` - Delete teacher (Admin only)

### Courses
- **GET** `/api/courses/` - List courses
- **POST** `/api/courses/` - Create course (Admin only)
- **GET** `/api/courses/{id}/` - Get course
- **PUT** `/api/courses/{id}/` - Update course
- **DELETE** `/api/courses/{id}/` - Delete course (Admin only)

### Enrollments
- **GET** `/api/courses/enrollments/` - List enrollments
- **POST** `/api/courses/enrollments/` - Create enrollment
- **GET** `/api/courses/enrollments/{id}/` - Get enrollment
- **PUT** `/api/courses/enrollments/{id}/` - Update enrollment
- **DELETE** `/api/courses/enrollments/{id}/` - Delete enrollment

## Project Structure

```
backend/
├── sms_backend/          # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI application
├── accounts/            # User & authentication
│   ├── models.py        # User model
│   ├── serializers.py   # User serializers
│   ├── views.py         # Auth views
│   ├── permissions.py   # Custom permissions
│   └── utils.py         # Helper functions
├── students/            # Student management
│   ├── models.py        # Student model
│   ├── serializers.py   # Student serializers
│   └── views.py         # Student views
├── teachers/            # Teacher management
│   ├── models.py        # Teacher model
│   ├── serializers.py   # Teacher serializers
│   └── views.py         # Teacher views
├── courses/             # Course & enrollment management
│   ├── models.py        # Course & Enrollment models
│   ├── serializers.py   # Course serializers
│   └── views.py         # Course views
└── manage.py
```

## Database Models

### User
- Custom user model with email authentication
- Roles: ADMIN, TEACHER, STUDENT
- Fields: email, username, first_name, last_name, role, phone_number, profile_picture

### Student
- One-to-one relationship with User
- Fields: student_id, date_of_birth, gender, grade, address, emergency contacts, GPA

### Teacher
- One-to-one relationship with User
- Fields: teacher_id, department, specialization, qualification, experience_years

### Course
- Many-to-one relationship with Teacher
- Fields: course_code, course_name, semester, academic_year, schedule, max_students

### Enrollment
- Many-to-one relationships with Student and Course
- Fields: status, grade, grade_points

## Authentication

JWT token-based authentication:
- Access token lifetime: 60 minutes (configurable)
- Refresh token lifetime: 24 hours (configurable)
- Tokens are automatically refreshed on the frontend

## Permissions

Custom permission classes:
- `IsAdmin` - Admin only
- `IsTeacher` - Teacher only
- `IsStudent` - Student only
- `IsAdminOrTeacher` - Admin or Teacher
- `IsOwnerOrAdmin` - Object owner or Admin
- `IsAdminOrReadOnly` - Admin can edit, others read-only

## Error Handling

Standardized error response format:
```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "details": {}
  }
}
```

Success response format:
```json
{
  "success": true,
  "message": "Success message",
  "data": {}
}
```
