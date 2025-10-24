# Frontend - Student Management System

React.js frontend with Vite, TailwindCSS, and JWT authentication.

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Setup environment:
```bash
copy .env.example .env
```

3. Run development server:
```bash
npm run dev
```

Application will run at: `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   │   ├── Layout.jsx   # Main layout with navigation
│   │   └── PrivateRoute.jsx  # Protected route wrapper
│   ├── contexts/        # React contexts
│   │   └── AuthContext.jsx   # Authentication context
│   ├── pages/          # Page components
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Students.jsx
│   │   ├── Teachers.jsx
│   │   └── Courses.jsx
│   ├── utils/          # Utilities
│   │   └── api.js      # Axios instance with interceptors
│   ├── App.jsx         # Main app component
│   ├── main.jsx        # Entry point
│   └── index.css       # Global styles
├── public/
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## Features

### Authentication
- JWT-based authentication
- Token refresh mechanism
- Protected routes
- Role-based access control

### Pages
- **Login** - User login with email/password
- **Register** - New user registration
- **Dashboard** - Overview with statistics
- **Students** - Student management (Admin/Teacher)
- **Teachers** - Teacher management (Admin/Teacher)
- **Courses** - Course browsing (All users)

### Components
- **Layout** - Main layout with navigation bar
- **PrivateRoute** - Route protection wrapper
- Responsive design with TailwindCSS

### API Integration
- Axios instance with interceptors
- Automatic token refresh
- Error handling
- Base URL configuration

## Authentication Flow

1. User logs in with email/password
2. Backend returns access and refresh tokens
3. Tokens stored in localStorage
4. Access token sent with each API request
5. On 401 error, refresh token used to get new access token
6. If refresh fails, user redirected to login

## Role-Based Access

### Admin
- Access to all pages
- Full CRUD operations
- User management

### Teacher
- Access to students, teachers, courses
- Can view and update records
- Cannot create/delete teachers or courses

### Student
- Access to dashboard and courses
- View own profile
- View enrolled courses

## Styling

- **TailwindCSS** for utility-first styling
- **Lucide React** for icons
- Responsive design
- Modern, clean UI

## API Client

Axios instance configured with:
- Base URL from environment
- Request interceptor (adds auth token)
- Response interceptor (handles token refresh)
- Error handling

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Variables

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## Building for Production

```bash
npm run build
```

Build output in `dist/` folder. Serve with any static file server.
