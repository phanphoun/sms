import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import api from '../utils/api'
import { Search, BookOpen } from 'lucide-react'

const Courses = () => {
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchCourses()
  }, [])

  const fetchCourses = async () => {
    try {
      const response = await api.get('/courses/')
      setCourses(response.data.data || response.data.results || [])
    } catch (error) {
      alert('Failed to fetch courses')
    } finally {
      setLoading(false)
    }
  }

  const filteredCourses = courses.filter(course =>
    course.course_code?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.course_name?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Courses</h1>
          <p className="text-gray-600 mt-2">Browse available courses</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="relative mb-6">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search courses..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {loading ? (
            <div className="text-center py-12">Loading...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredCourses.map((course) => (
                <div key={course.id} className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between mb-4">
                    <BookOpen className="w-8 h-8 text-primary-600" />
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${course.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                      {course.status}
                    </span>
                  </div>
                  <h3 className="font-bold text-lg mb-2">{course.course_code}</h3>
                  <p className="text-gray-600 mb-4">{course.course_name}</p>
                  <div className="space-y-2 text-sm text-gray-600">
                    <p>Credits: {course.credits}</p>
                    <p>Teacher: {course.teacher?.full_name || 'TBA'}</p>
                    <p>Enrolled: {course.enrolled_count}/{course.max_students}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}

export default Courses
