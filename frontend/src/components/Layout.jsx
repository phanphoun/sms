import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { LogOut, Users, GraduationCap, BookOpen, Home } from 'lucide-react'

const Layout = ({ children }) => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-primary-600 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-8">
              <h1 className="text-xl font-bold">SMS</h1>
              <div className="flex space-x-4">
                <Link to="/" className="flex items-center px-3 py-2 rounded-md hover:bg-primary-700"><Home className="w-4 h-4 mr-2" />Dashboard</Link>
                {(user?.role === 'ADMIN' || user?.role === 'TEACHER') && (
                  <>
                    <Link to="/students" className="flex items-center px-3 py-2 rounded-md hover:bg-primary-700"><Users className="w-4 h-4 mr-2" />Students</Link>
                    <Link to="/teachers" className="flex items-center px-3 py-2 rounded-md hover:bg-primary-700"><GraduationCap className="w-4 h-4 mr-2" />Teachers</Link>
                  </>
                )}
                <Link to="/courses" className="flex items-center px-3 py-2 rounded-md hover:bg-primary-700"><BookOpen className="w-4 h-4 mr-2" />Courses</Link>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span>{user?.full_name} ({user?.role})</span>
              <button onClick={handleLogout} className="flex items-center px-4 py-2 rounded-md bg-red-600 hover:bg-red-700"><LogOut className="w-4 h-4 mr-2" />Logout</button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">{children}</main>
    </div>
  )
}

export default Layout
