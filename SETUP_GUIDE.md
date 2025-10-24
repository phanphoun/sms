# Complete Setup Guide - Student Management System

This guide walks you through setting up the entire SMS system from scratch.

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher installed
- Node.js 16 or higher installed
- MySQL 8.0 or higher installed
- Git installed
- A text editor (VS Code recommended)

## Step 1: Database Setup

### Install MySQL
If not already installed, download and install MySQL from [mysql.com](https://dev.mysql.com/downloads/)

### Create Database
1. Open MySQL command line or MySQL Workbench
2. Run the following commands:

```sql
CREATE DATABASE sms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Optional: Create a dedicated user
CREATE USER 'sms_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON sms_db.* TO 'sms_user'@'localhost';
FLUSH PRIVILEGES;
```

## Step 2: Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` file with your settings:
```env
SECRET_KEY=your-very-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=sms_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Start Backend Server
```bash
python manage.py runserver
```

Backend should now be running at `http://localhost:8000`

## Step 3: Frontend Setup

### 1. Open New Terminal and Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

If you encounter any errors, try:
```bash
npm install --legacy-peer-deps
```

### 3. Configure Environment Variables
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

The default `.env` should work:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### 4. Start Frontend Development Server
```bash
npm run dev
```

Frontend should now be running at `http://localhost:3000`

## Step 4: Verify Installation

### 1. Access the Application
Open your browser and go to: `http://localhost:3000`

### 2. Test Login
Use the superuser credentials you created to log in.

### 3. Test API
Access Django admin: `http://localhost:8000/admin`

## Step 5: Create Initial Data (Optional)

### Using Django Admin
1. Go to `http://localhost:8000/admin`
2. Log in with superuser credentials
3. Create sample students, teachers, and courses

### Using API
You can also use the frontend application to:
1. Register new users
2. Create student profiles
3. Create teacher profiles
4. Create courses

## Common Issues and Solutions

### Issue: MySQL Connection Error
**Solution**: 
- Verify MySQL is running
- Check database credentials in `.env`
- Ensure database exists: `SHOW DATABASES;`

### Issue: Module Not Found (Python)
**Solution**: 
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

### Issue: npm Install Errors
**Solution**:
- Clear npm cache: `npm cache clean --force`
- Try: `npm install --legacy-peer-deps`
- Update Node.js to latest LTS version

### Issue: Port Already in Use
**Solution**:
- Backend: Change port with `python manage.py runserver 8001`
- Frontend: Change port in `vite.config.js`

### Issue: CORS Errors
**Solution**:
- Verify CORS settings in `backend/sms_backend/settings.py`
- Ensure frontend URL is in `CORS_ALLOWED_ORIGINS`

## Next Steps

### For Development
1. Create test data through the admin panel
2. Test all features (login, register, CRUD operations)
3. Review API endpoints in backend README
4. Customize UI components as needed

### For Production
1. Set `DEBUG=False` in backend `.env`
2. Change `SECRET_KEY` to a strong random value
3. Update `ALLOWED_HOSTS` with your domain
4. Configure proper database credentials
5. Build frontend: `npm run build`
6. Set up web server (nginx/apache)
7. Use gunicorn for Django
8. Configure SSL certificates

## Testing the System

### Test as Admin
1. Log in with superuser account
2. Access all pages (Dashboard, Students, Teachers, Courses)
3. Create a new student
4. Create a new teacher
5. Create a new course

### Test as Teacher
1. Register a new account with Teacher role
2. Have admin create teacher profile for the user
3. Log in and verify access to students and courses

### Test as Student
1. Register a new account with Student role
2. Have admin create student profile for the user
3. Log in and verify limited access
4. View available courses

## Support

If you encounter issues:
1. Check the error messages carefully
2. Review the README files in backend and frontend folders
3. Verify all prerequisites are installed
4. Check that both servers are running
5. Look for typos in configuration files

## Database Schema Reference

```
Users (accounts_user)
├── id (PK)
├── email (unique)
├── username (unique)
├── password (hashed)
├── first_name
├── last_name
├── role (ADMIN/TEACHER/STUDENT)
└── ... other fields

Students (students)
├── id (PK)
├── user_id (FK → Users)
├── student_id (unique)
├── date_of_birth
├── gender
├── grade
├── gpa
└── ... other fields

Teachers (teachers)
├── id (PK)
├── user_id (FK → Users)
├── teacher_id (unique)
├── department
├── specialization
└── ... other fields

Courses (courses)
├── id (PK)
├── teacher_id (FK → Teachers)
├── course_code (unique)
├── course_name
├── semester
├── academic_year
└── ... other fields

Enrollments (enrollments)
├── id (PK)
├── student_id (FK → Students)
├── course_id (FK → Courses)
├── status
├── grade
└── grade_points
```

## Congratulations!

Your Student Management System is now set up and running. Start exploring the features and customize it to your needs!
