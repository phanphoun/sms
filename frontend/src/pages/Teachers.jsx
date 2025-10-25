import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import api from '../utils/api'
import { Search } from 'lucide-react'

const Teachers = () => {
  const [teachers, setTeachers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchTeachers()
  }, [])

  const fetchTeachers = async () => {
    try {
      const response = await api.get('/teachers/')
      setTeachers(response.data.data || response.data.results || [])
    } catch (error) {
      alert('Failed to fetch teachers')
    } finally {
      setLoading(false)
    }
  }

  const filteredTeachers = teachers.filter(teacher =>
    teacher.teacher_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    teacher.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    teacher.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    teacher.specialization?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Teachers</h1>
            <p className="text-gray-600 mt-2">Manage teacher records</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center space-x-4 mb-6">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search teachers..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          {loading ? (
            <div className="text-center py-12 text-gray-500">Loading teachers...</div>
          ) : filteredTeachers.length === 0 ? (
            <div className="text-center py-12 text-gray-500">No teachers found</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Teacher ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Department</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Specialization</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Experience</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {filteredTeachers.map((teacher) => (
                    <tr key={teacher.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{teacher.teacher_id}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{teacher.full_name}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{teacher.email}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{teacher.department}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{teacher.specialization}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{teacher.experience_years} years</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${teacher.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                          {teacher.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}

export default Teachers
