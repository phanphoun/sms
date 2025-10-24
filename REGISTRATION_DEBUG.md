# Registration Error - Debugging Guide

## Current Setup Status
✅ Database connected: `sms_db`  
✅ All tables created (14 tables)  
✅ Frontend code looks correct  
✅ Backend endpoint configured  
✅ CORS configured for localhost:5173 and localhost:3000  

---

## Common Registration Errors & Solutions

### 1. **Password Validation Error**
**Error**: "This password is too common" or "Password must contain..."

**Solution**: Use a stronger password with:
- At least 8 characters
- Mix of uppercase and lowercase letters
- Numbers
- Special characters

**Example strong password**: `Student123!`

---

### 2. **CORS Error**
**Error**: "Access to XMLHttpRequest blocked by CORS policy"

**Check**:
1. Backend server is running on `http://localhost:8000`
2. Frontend is running on `http://localhost:5173` or `http://localhost:3000`
3. CORS settings in backend allow your frontend URL

**Fix**: Already configured in `settings.py` lines 175-203

---

### 3. **Server Not Running**
**Error**: "Network Error" or "ERR_CONNECTION_REFUSED"

**Solution**:
```bash
cd c:\Users\PHOUN.PHAN\Desktop\SMS\sms\backend
sms\Scripts\activate
python manage.py runserver
```

Keep this terminal open while using the app.

---

### 4. **Email/Username Already Exists**
**Error**: "A user with this email already exists"

**Solution**: Use a different email or username that hasn't been registered before.

---

### 5. **Missing Required Fields**
**Error**: "This field is required"

**Required fields**:
- Email
- Username
- Password
- Password2 (confirmation)
- First Name
- Last Name

---

## How to Test Registration

### Method 1: Through Frontend (Recommended)

1. **Start Backend**:
```bash
cd backend
sms\Scripts\activate
python manage.py runserver
```

2. **Start Frontend** (in new terminal):
```bash
cd frontend
npm run dev
```

3. **Open browser**: http://localhost:5173/register

4. **Fill in the form**:
   - First Name: John
   - Last Name: Doe
   - Email: john.doe@example.com
   - Username: johndoe
   - Phone: 1234567890
   - Password: Student123!
   - Confirm Password: Student123!
   - Role: Student

5. **Click "Create Account"**

---

### Method 2: Test API Directly (For Debugging)

Run this test script:
```bash
cd backend
sms\Scripts\activate
pip install requests  # if not installed
python test_registration.py
```

This will show you the exact error from the API.

---

### Method 3: Test with curl

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "Student123!",
    "password2": "Student123!",
    "first_name": "Test",
    "last_name": "User",
    "phone_number": "1234567890",
    "role": "STUDENT"
  }'
```

---

## Checking Server Status

### Is Backend Running?
```bash
# Test if server responds
curl http://localhost:8000/api/auth/register/
```

Expected: Should return "Method GET not allowed" (means server is running)

### Check Backend Logs
Look at the terminal where you ran `python manage.py runserver`.  
You should see:
```
Starting development server at http://127.0.0.1:8000/
```

And when you try to register, you'll see logs like:
```
[24/Oct/2025 18:00:00] "POST /api/auth/register/ HTTP/1.1" 201 150
```

The `201` means success. Other codes:
- `400` = Bad request (validation error)
- `500` = Server error
- `403` = Forbidden
- `404` = Endpoint not found

---

## What Error Are You Seeing?

### A. Frontend Shows Error Message
**Take note of the exact error message displayed**

Example: "Password fields didn't match"  
→ Make sure both password fields have the same value

### B. Network Error in Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for red error messages
4. Check Network tab → Click the failed request → See the response

### C. Backend Terminal Shows Error
Copy the entire traceback and look for the last line with the actual error.

---

## Quick Fix Checklist

- [ ] Backend server is running (`python manage.py runserver`)
- [ ] Frontend server is running (`npm run dev`)
- [ ] Using a strong password (8+ chars, mixed case, numbers, symbols)
- [ ] Password and Confirm Password match
- [ ] Email hasn't been used before
- [ ] Username hasn't been used before
- [ ] All required fields are filled

---

## Still Not Working?

### Get Detailed Error Information

1. **Check browser console** (F12 → Console tab)
2. **Check browser network tab** (F12 → Network tab → Look for failed requests)
3. **Check backend terminal** for error messages
4. **Run the test script**: `python test_registration.py`

### Share This Information:
- Exact error message from frontend
- Backend terminal output
- Browser console errors
- Response from test_registration.py

---

## Next Steps After Successful Registration

1. **Create a superuser** (for admin access):
```bash
python manage.py createsuperuser
```

2. **Access admin panel**: http://localhost:8000/admin

3. **View registered users**: Admin panel → Users

4. **Test login** with your newly created account

---

## API Endpoints Reference

- Register: `POST /api/auth/register/`
- Login: `POST /api/auth/login/`
- Profile: `GET /api/auth/profile/`
- Logout: `POST /api/auth/logout/`

---

## Contact Information

If you're still having issues, provide:
1. The exact error message
2. Screenshot of the error
3. Backend terminal logs
4. Browser console logs (F12)
