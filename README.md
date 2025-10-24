# Student Management System (SMS)

A comprehensive web-based Student Management System built with Django REST Framework, React.js, and MySQL. This system provides role-based access control for managing students, teachers, and courses.

## 🎯 Features

### Core Features
- **User Authentication**: Secure JWT-based authentication system
- **Role-Based Access Control**: Three user roles (Admin, Teacher, Student)
- **Student Management**: Complete CRUD operations for student records
- **Teacher Management**: Manage teacher profiles and assignments
- **Course Management**: Create and manage courses with enrollments
- **Grade Management**: Track student grades and GPA

### Technical Features
- RESTful API architecture
- JWT token authentication with refresh tokens
- Responsive UI with TailwindCSS
- Form validation and error handling
- Database indexing for performance
- Secure password hashing

## 📋 Database Schema

### Users Table
- **Primary Key**: `id` (BigAutoField)
- **Fields**: email, username, password, first_name, last_name, role, phone_number, profile_picture
- **Roles**: ADMIN, TEACHER, STUDENT

### Students Table
- **Primary Key**: `id` (BigAutoField)
- **Foreign Key**: `user_id` → Users
- **Fields**: student_id, date_of_birth, gender, grade, address, emergency contacts, GPA

### Teachers Table
- **Primary Key**: `id` (BigAutoField)
- **Foreign Key**: `user_id` → Users
- **Fields**: teacher_id, department, specialization, qualification, experience_years

### Courses Table
- **Primary Key**: `id` (BigAutoField)
- **Foreign Key**: `teacher_id` → Teachers
- **Fields**: course_code, course_name, semester, academic_year, schedule, max_students

### Enrollments Table
- **Primary Key**: `id` (BigAutoField)
- **Foreign Keys**: `student_id` → Students, `course_id` → Courses
- **Fields**: status, grade, grade_points

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Git

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
copy .env.example .env
# Edit .env with your database credentials
```

5. **Create MySQL database**
```sql
CREATE DATABASE sms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Run development server**
```bash
python manage.py runserver
```

Backend will run at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
```bash
copy .env.example .env
# Edit .env if needed
```

4. **Run development server**
```bash
npm run dev
```

Frontend will run at: `http://localhost:3000`

## 📡 API Endpoints

### Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `POST /api/auth/change-password/` - Change password

### Student Endpoints (Admin/Teacher access)
- `GET /api/students/` - List all students
- `POST /api/students/` - Create new student
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student
- `GET /api/students/my-profile/` - Get own profile (Students)

### Teacher Endpoints (Admin/Teacher access)
- `GET /api/teachers/` - List all teachers
- `POST /api/teachers/` - Create new teacher (Admin only)
- `GET /api/teachers/{id}/` - Get teacher details
- `PUT /api/teachers/{id}/` - Update teacher
- `DELETE /api/teachers/{id}/` - Delete teacher (Admin only)
- `GET /api/teachers/my-profile/` - Get own profile (Teachers)

### Course Endpoints
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create new course (Admin only)
- `GET /api/courses/{id}/` - Get course details
- `PUT /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course (Admin only)

### Enrollment Endpoints
- `GET /api/courses/enrollments/` - List enrollments
- `POST /api/courses/enrollments/` - Create enrollment
- `GET /api/courses/enrollments/{id}/` - Get enrollment details
- `PUT /api/courses/enrollments/{id}/` - Update enrollment
- `DELETE /api/courses/enrollments/{id}/` - Delete enrollment

## 🔐 Role-Based Access Control

### Admin
- Full system access
- Manage all users, students, teachers, and courses
- Create and delete records
- View all data

### Teacher
- View and manage students
- View and manage courses
- Update grades and enrollments
- Cannot create/delete teachers or courses

### Student
- View own profile
- View enrolled courses
- View grades
- Limited access to system features

## 🎨 Frontend Routes

- `/login` - Login page
- `/register` - Registration page
- `/` - Dashboard (Protected)
- `/students` - Student list (Admin/Teacher only)
- `/teachers` - Teacher list (Admin/Teacher only)
- `/courses` - Course list (All authenticated users)

## ⚙️ Configuration

### Backend Configuration
Edit `backend/.env`:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=sms_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### Frontend Configuration
Edit `frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 🛡️ Security Features

- Password hashing with Django's built-in system
- JWT token-based authentication
- Token refresh mechanism
- CORS configuration
- SQL injection prevention through ORM
- XSS protection
- CSRF protection
- Input validation and sanitization

## 🧪 Testing

### Backend Testing
```bash
python manage.py test
```

### Frontend Testing
```bash
npm run test
```

## 📦 Building for Production

### Backend
```bash
python manage.py collectstatic
# Deploy using gunicorn, nginx, etc.
```

### Frontend
```bash
npm run build
# Serve the dist folder with nginx or similar
```

## 🐛 Error Handling

The system implements comprehensive error handling:
- **Frontend**: Try-catch blocks with user-friendly error messages
- **Backend**: Custom exception handler with standardized error responses
- **Validation**: Form validation on both client and server side
- **API Errors**: Consistent error response format

### Error Response Format
```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "details": {}
  }
}
```

## 📚 Code Structure

### Backend Structure
```
backend/
├── sms_backend/          # Project settings
├── accounts/             # User authentication & management
├── students/             # Student management
├── teachers/             # Teacher management
├── courses/              # Course & enrollment management
└── manage.py
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/       # Reusable components
│   ├── contexts/         # React contexts (Auth)
│   ├── pages/           # Page components
│   ├── utils/           # Utilities (API client)
│   ├── App.jsx          # Main app component
│   └── main.jsx         # Entry point
└── public/
```

## 🔧 Best Practices Implemented

1. **Separation of Concerns**: Clear separation between models, serializers, views
2. **DRY Principle**: Reusable components and utilities
3. **Security First**: All sensitive operations require authentication
4. **Error Handling**: Comprehensive error handling at all levels
5. **Code Documentation**: Docstrings and comments throughout
6. **RESTful Design**: Following REST principles for API design
7. **Responsive Design**: Mobile-first approach with TailwindCSS

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as a learning project for Student Management System

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements.

## 📞 Support

For support or questions, please open an issue in the repository.
