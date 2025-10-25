import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { useAuth } from '../contexts/AuthContext'
import api from '../utils/api'
import { Users, GraduationCap, BookOpen, TrendingUp } from 'lucide-react'

const Dashboard = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState({ students: 0, teachers: 0, courses: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      if (user.role === 'ADMIN' || user.role === 'TEACHER') {
        const [studentsRes, teachersRes, coursesRes] = await Promise.all([
          api.get('/students/'),
          api.get('/teachers/'),
          api.get('/courses/')
        ])
        setStats({
          students: studentsRes.data.data?.length || studentsRes.data.results?.length || 0,
          teachers: teachersRes.data.data?.length || teachersRes.data.results?.length || 0,
          courses: coursesRes.data.data?.length || coursesRes.data.results?.length || 0
        })
      }
    } catch (error) {
      // Silently handle error for stats
    } finally {
      setLoading(false)
    }
  }

  const StatCard = ({ icon: Icon, title, value, color }) => (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm font-medium">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <div className={`p-3 rounded-full ${color}`}>
          <Icon className="w-8 h-8 text-white" />
        </div>
      </div>
    </div>
  )

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Welcome back, {user?.full_name}!</p>
        </div>

        {(user?.role === 'ADMIN' || user?.role === 'TEACHER') && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StatCard icon={Users} title="Total Students" value={stats.students} color="bg-blue-500" />
            <StatCard icon={GraduationCap} title="Total Teachers" value={stats.teachers} color="bg-green-500" />
            <StatCard icon={BookOpen} title="Total Courses" value={stats.courses} color="bg-purple-500" />
          </div>
        )}

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {user?.role === 'STUDENT' && (
              <a href="/courses" className="p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:shadow-md transition-all">
                <BookOpen className="w-8 h-8 text-primary-600 mb-2" />
                <h3 className="font-semibold">View My Courses</h3>
                <p className="text-sm text-gray-600">See your enrolled courses</p>
              </a>
            )}
            {(user?.role === 'ADMIN' || user?.role === 'TEACHER') && (
              <>
                <a href="/students" className="p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:shadow-md transition-all">
                  <Users className="w-8 h-8 text-primary-600 mb-2" />
                  <h3 className="font-semibold">Manage Students</h3>
                  <p className="text-sm text-gray-600">View and manage student records</p>
                </a>
                <a href="/teachers" className="p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:shadow-md transition-all">
                  <GraduationCap className="w-8 h-8 text-primary-600 mb-2" />
                  <h3 className="font-semibold">Manage Teachers</h3>
                  <p className="text-sm text-gray-600">View and manage teacher records</p>
                </a>
                <a href="/courses" className="p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:shadow-md transition-all">
                  <BookOpen className="w-8 h-8 text-primary-600 mb-2" />
                  <h3 className="font-semibold">Manage Courses</h3>
                  <p className="text-sm text-gray-600">View and manage courses</p>
                </a>
              </>
            )}
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default Dashboard
