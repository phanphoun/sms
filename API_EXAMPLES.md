# API Usage Examples

Complete examples of API requests and responses for the Student Management System.

## Authentication

### Register New User

**Request:**
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "role": "STUDENT"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "john.doe@example.com",
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "role": "STUDENT",
      "is_active": true
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
}
```

### Login

**Request:**
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "john.doe@example.com",
      "username": "johndoe",
      "full_name": "John Doe",
      "role": "STUDENT"
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
}
```

### Refresh Token

**Request:**
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Get Profile

**Request:**
```http
GET /api/auth/profile/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response:**
```json
{
  "success": true,
  "message": "Profile retrieved successfully",
  "data": {
    "id": 1,
    "email": "john.doe@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "role": "STUDENT",
    "is_active": true,
    "date_joined": "2024-01-15T10:30:00Z"
  }
}
```

## Student Management

### Create Student Profile

**Request:**
```http
POST /api/students/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "user_id": 1,
  "student_id": "STU2024001",
  "date_of_birth": "2005-06-15",
  "gender": "M",
  "grade": "10",
  "address": "123 Main St, City, Country",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+1234567891",
  "emergency_contact_relation": "Mother",
  "gpa": 3.50
}
```

**Response:**
```json
{
  "success": true,
  "message": "Student created successfully",
  "data": {
    "id": 1,
    "student_id": "STU2024001",
    "user": {
      "id": 1,
      "email": "john.doe@example.com",
      "full_name": "John Doe"
    },
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "date_of_birth": "2005-06-15",
    "age": 18,
    "gender": "M",
    "grade": "10",
    "gpa": 3.50,
    "is_active": true,
    "enrollment_date": "2024-01-15T10:30:00Z"
  }
}
```

### List Students

**Request:**
```http
GET /api/students/?grade=10&search=john
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response:**
```json
{
  "success": true,
  "message": "Students retrieved successfully",
  "data": [
    {
      "id": 1,
      "student_id": "STU2024001",
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "grade": "10",
      "gpa": 3.50,
      "is_active": true
    }
  ]
}
```

### Update Student

**Request:**
```http
PATCH /api/students/1/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "gpa": 3.75,
  "grade": "11"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Student updated successfully",
  "data": {
    "id": 1,
    "student_id": "STU2024001",
    "full_name": "John Doe",
    "grade": "11",
    "gpa": 3.75
  }
}
```

## Teacher Management

### Create Teacher Profile

**Request:**
```http
POST /api/teachers/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "user_id": 2,
  "teacher_id": "TCH2024001",
  "department": "MATH",
  "specialization": "Calculus and Algebra",
  "qualification": "PhD in Mathematics",
  "experience_years": 10,
  "office_room": "A-301"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Teacher created successfully",
  "data": {
    "id": 1,
    "teacher_id": "TCH2024001",
    "user": {
      "id": 2,
      "email": "teacher@example.com",
      "full_name": "Dr. Smith"
    },
    "full_name": "Dr. Smith",
    "department": "MATH",
    "specialization": "Calculus and Algebra",
    "experience_years": 10,
    "is_active": true
  }
}
```

### List Teachers

**Request:**
```http
GET /api/teachers/?department=MATH
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response:**
```json
{
  "success": true,
  "message": "Teachers retrieved successfully",
  "data": [
    {
      "id": 1,
      "teacher_id": "TCH2024001",
      "full_name": "Dr. Smith",
      "department": "MATH",
      "specialization": "Calculus and Algebra",
      "experience_years": 10
    }
  ]
}
```

## Course Management

### Create Course

**Request:**
```http
POST /api/courses/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "course_code": "MATH101",
  "course_name": "Introduction to Calculus",
  "description": "Basic calculus concepts and applications",
  "teacher_id": 1,
  "credits": 3,
  "semester": "1",
  "academic_year": "2024-2025",
  "schedule": "Mon/Wed/Fri 10:00-11:30",
  "room": "B-201",
  "max_students": 30,
  "status": "ACTIVE"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Course created successfully",
  "data": {
    "id": 1,
    "course_code": "MATH101",
    "course_name": "Introduction to Calculus",
    "teacher": {
      "id": 1,
      "full_name": "Dr. Smith"
    },
    "credits": 3,
    "semester": "1",
    "academic_year": "2024-2025",
    "max_students": 30,
    "enrolled_count": 0,
    "is_full": false,
    "status": "ACTIVE"
  }
}
```

### List Courses

**Request:**
```http
GET /api/courses/?semester=1&academic_year=2024-2025
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response:**
```json
{
  "success": true,
  "message": "Courses retrieved successfully",
  "data": [
    {
      "id": 1,
      "course_code": "MATH101",
      "course_name": "Introduction to Calculus",
      "teacher": {
        "full_name": "Dr. Smith"
      },
      "credits": 3,
      "enrolled_count": 15,
      "max_students": 30,
      "is_full": false,
      "status": "ACTIVE"
    }
  ]
}
```

## Enrollment Management

### Create Enrollment

**Request:**
```http
POST /api/courses/enrollments/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "student_id": 1,
  "course_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "message": "Enrollment created successfully",
  "data": {
    "id": 1,
    "student": {
      "id": 1,
      "student_id": "STU2024001",
      "full_name": "John Doe"
    },
    "course": {
      "id": 1,
      "course_code": "MATH101",
      "course_name": "Introduction to Calculus"
    },
    "enrollment_date": "2024-01-15T10:30:00Z",
    "status": "ENROLLED",
    "grade": null,
    "grade_points": null
  }
}
```

### Update Enrollment (Add Grade)

**Request:**
```http
PATCH /api/courses/enrollments/1/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "grade": "A",
  "status": "COMPLETED"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Enrollment updated successfully",
  "data": {
    "id": 1,
    "student": {
      "full_name": "John Doe"
    },
    "course": {
      "course_code": "MATH101"
    },
    "status": "COMPLETED",
    "grade": "A",
    "grade_points": 4.00
  }
}
```

## Error Responses

### Validation Error

```json
{
  "success": false,
  "error": {
    "message": "Validation error",
    "details": {
      "email": ["This field is required."],
      "password": ["Password must be at least 8 characters."]
    }
  }
}
```

### Authentication Error

```json
{
  "success": false,
  "error": {
    "message": "Invalid credentials",
    "details": {
      "email": "Email or password is incorrect"
    }
  }
}
```

### Permission Error

```json
{
  "success": false,
  "error": {
    "message": "Only administrators can create teacher profiles",
    "details": null
  }
}
```

## Using with cURL

### Login Example
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "adminpass123"
  }'
```

### Authenticated Request Example
```bash
curl -X GET http://localhost:8000/api/students/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## Using with JavaScript/Axios

```javascript
// Login
const response = await axios.post('http://localhost:8000/api/auth/login/', {
  email: 'admin@example.com',
  password: 'adminpass123'
});

const { access, refresh } = response.data.data.tokens;

// Authenticated request
const students = await axios.get('http://localhost:8000/api/students/', {
  headers: {
    'Authorization': `Bearer ${access}`
  }
});
```

## Query Parameters

### Filtering
- `?grade=10` - Filter by grade
- `?department=MATH` - Filter by department
- `?status=ACTIVE` - Filter by status
- `?is_active=true` - Filter by active status

### Searching
- `?search=john` - Search across multiple fields

### Ordering
- `?ordering=gpa` - Order by GPA ascending
- `?ordering=-gpa` - Order by GPA descending
- `?ordering=enrollment_date` - Order by enrollment date

### Pagination
- `?page=1` - Get first page
- `?page_size=20` - Set page size (default: 10)
