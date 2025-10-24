# Quick Reference Guide

## Common Commands

### Backend Commands

**Start Server**
```bash
cd backend
python manage.py runserver
```

**Create Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Create Superuser**
```bash
python manage.py createsuperuser
```

**Create Normal User (Django Shell)**
```bash
python manage.py shell
```
```python
from accounts.models import User
user = User.objects.create_user(
    email='test@example.com',
    username='testuser',
    password='testpass123',
    first_name='Test',
    last_name='User',
    role='STUDENT'
)
```

**Reset Database**
```bash
python manage.py flush
python manage.py migrate
```

### Frontend Commands

**Start Dev Server**
```bash
cd frontend
npm run dev
```

**Build for Production**
```bash
npm run build
```

**Install New Package**
```bash
npm install package-name
```

## Common API Requests

### Get Access Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

### List Students
```bash
curl http://localhost:8000/api/students/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Student
```bash
curl -X POST http://localhost:8000/api/students/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "student_id": "STU001",
    "date_of_birth": "2005-01-01",
    "gender": "M",
    "grade": "10",
    "emergency_contact_name": "Parent",
    "emergency_contact_phone": "123456",
    "emergency_contact_relation": "Father"
  }'
```

## Database Queries (Django Shell)

**List All Users**
```python
from accounts.models import User
User.objects.all()
```

**Get User by Email**
```python
user = User.objects.get(email='test@example.com')
```

**List All Students**
```python
from students.models import Student
Student.objects.all()
```

**Create Student Profile**
```python
from students.models import Student
from accounts.models import User

user = User.objects.get(email='student@example.com')
student = Student.objects.create(
    user=user,
    student_id='STU001',
    date_of_birth='2005-01-01',
    gender='M',
    grade='10',
    emergency_contact_name='Parent',
    emergency_contact_phone='123456',
    emergency_contact_relation='Father'
)
```

**Get Students by Grade**
```python
Student.objects.filter(grade='10')
```

**Update Student GPA**
```python
student = Student.objects.get(student_id='STU001')
student.gpa = 3.75
student.save()
```

## Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=sms_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## File Locations

### Backend Key Files
- Models: `backend/[app]/models.py`
- Views: `backend/[app]/views.py`
- Serializers: `backend/[app]/serializers.py`
- URLs: `backend/[app]/urls.py`
- Settings: `backend/sms_backend/settings.py`

### Frontend Key Files
- Pages: `frontend/src/pages/`
- Components: `frontend/src/components/`
- API Client: `frontend/src/utils/api.js`
- Auth Context: `frontend/src/contexts/AuthContext.jsx`
- Main App: `frontend/src/App.jsx`

## Default Ports
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- MySQL: localhost:3306

## Default Credentials
Create your own using:
```bash
python manage.py createsuperuser
```

## Useful Django Commands

**Check for issues**
```bash
python manage.py check
```

**Show migrations**
```bash
python manage.py showmigrations
```

**Create app**
```bash
python manage.py startapp appname
```

**Collect static files**
```bash
python manage.py collectstatic
```

**Run tests**
```bash
python manage.py test
```

## Troubleshooting

**Port already in use**
```bash
# Find process on Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Find process on Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Reset migrations**
```bash
# Delete migration files (keep __init__.py)
# Delete database
# Recreate database
python manage.py makemigrations
python manage.py migrate
```

**Clear npm cache**
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## User Roles and Access

| Feature | Admin | Teacher | Student |
|---------|-------|---------|---------|
| View Students | ✅ | ✅ | ❌ |
| Create Students | ✅ | ✅ | ❌ |
| Edit Students | ✅ | ✅ | ❌ |
| Delete Students | ✅ | ❌ | ❌ |
| View Teachers | ✅ | ✅ | ❌ |
| Create Teachers | ✅ | ❌ | ❌ |
| View Courses | ✅ | ✅ | ✅ |
| Create Courses | ✅ | ❌ | ❌ |
| Manage Grades | ✅ | ✅ | ❌ |
| View Own Profile | ✅ | ✅ | ✅ |

## API Response Formats

**Success Response**
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {}
}
```

**Error Response**
```json
{
  "success": false,
  "error": {
    "message": "Error message",
    "details": {}
  }
}
```

## Git Commands (for version control)

```bash
# Initialize repo
git init
git add .
git commit -m "Initial commit"

# Create branch
git checkout -b feature-name

# Push to remote
git remote add origin <url>
git push -u origin main
```

## Production Deployment Checklist

- [ ] Set DEBUG=False
- [ ] Change SECRET_KEY
- [ ] Update ALLOWED_HOSTS
- [ ] Configure database for production
- [ ] Set up static files serving
- [ ] Configure HTTPS
- [ ] Set up backup system
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Test all endpoints
- [ ] Build frontend: `npm run build`
- [ ] Configure web server (nginx/apache)
- [ ] Set up environment variables securely

## Performance Tips

**Backend**
- Use select_related() for foreign keys
- Use prefetch_related() for many-to-many
- Add database indexes
- Enable pagination
- Use caching (Redis)

**Frontend**
- Lazy load components
- Optimize images
- Use code splitting
- Minimize bundle size
- Enable gzip compression

## Security Checklist

- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS in production
- [ ] Validate all inputs
- [ ] Use parameterized queries
- [ ] Implement rate limiting
- [ ] Keep dependencies updated
- [ ] Use environment variables
- [ ] Enable CORS properly
- [ ] Hash passwords
- [ ] Implement token expiration
