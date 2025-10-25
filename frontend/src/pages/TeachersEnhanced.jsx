import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import api from '../utils/api'
import { Search, Plus, Edit, Trash2, X, Eye, UserPlus, Filter, Download, Award } from 'lucide-react'

const TeachersEnhanced = () => {
  const [teachers, setTeachers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterDepartment, setFilterDepartment] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [showDetailModal, setShowDetailModal] = useState(false)
  const [currentTeacher, setCurrentTeacher] = useState(null)
  const [formData, setFormData] = useState({
    teacher_id: '',
    email: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    department: '',
    specialization: '',
    qualification: '',
    experience_years: ''
  })

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

  const handleCreate = () => {
    setCurrentTeacher(null)
    setFormData({
      teacher_id: '',
      email: '',
      first_name: '',
      last_name: '',
      phone_number: '',
      department: '',
      specialization: '',
      qualification: '',
      experience_years: ''
    })
    setShowModal(true)
  }

  const handleEdit = (teacher) => {
    setCurrentTeacher(teacher)
    setFormData({
      teacher_id: teacher.teacher_id || '',
      email: teacher.email || '',
      first_name: teacher.first_name || '',
      last_name: teacher.last_name || '',
      phone_number: teacher.phone_number || '',
      department: teacher.department || '',
      specialization: teacher.specialization || '',
      qualification: teacher.qualification || '',
      experience_years: teacher.experience_years || ''
    })
    setShowModal(true)
  }

  const handleViewDetails = (teacher) => {
    setCurrentTeacher(teacher)
    setShowDetailModal(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (currentTeacher) {
        await api.put(`/teachers/${currentTeacher.id}/`, formData)
        alert('Teacher updated successfully!')
      } else {
        await api.post('/teachers/', formData)
        alert('Teacher created successfully!')
      }
      setShowModal(false)
      fetchTeachers()
    } catch (error) {
      alert(error.response?.data?.error?.message || 'Failed to save teacher')
    }
  }

  const handleDelete = async (teacher) => {
    if (!confirm(`Are you sure you want to delete ${teacher.full_name}?`)) return
    
    try {
      await api.delete(`/teachers/${teacher.id}/`)
      alert('Teacher deleted successfully!')
      fetchTeachers()
    } catch (error) {
      alert('Failed to delete teacher')
    }
  }

  const handleExport = () => {
    const csv = [
      ['Teacher ID', 'Name', 'Email', 'Department', 'Specialization', 'Experience', 'Status'],
      ...filteredTeachers.map(t => [
        t.teacher_id,
        t.full_name,
        t.email,
        t.department,
        t.specialization,
        `${t.experience_years} years`,
        t.is_active ? 'Active' : 'Inactive'
      ])
    ].map(row => row.join(',')).join('\n')
    
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'teachers.csv'
    a.click()
  }

  const departments = [...new Set(teachers.map(t => t.department).filter(Boolean))]

  const filteredTeachers = teachers.filter(teacher => {
    const matchesSearch = teacher.teacher_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      teacher.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      teacher.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      teacher.specialization?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesDepartment = !filterDepartment || teacher.department === filterDepartment
    return matchesSearch && matchesDepartment
  })

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Teachers Management</h1>
            <p className="text-gray-600 mt-2">Manage teacher records and information</p>
          </div>
          <button
            onClick={handleCreate}
            className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            <UserPlus className="w-5 h-5" />
            Add Teacher
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex flex-wrap items-center gap-4 mb-6">
            <div className="flex-1 min-w-[200px] relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search teachers..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="flex items-center gap-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <select
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                value={filterDepartment}
                onChange={(e) => setFilterDepartment(e.target.value)}
              >
                <option value="">All Departments</option>
                {departments.map(dept => (
                  <option key={dept} value={dept}>{dept}</option>
                ))}
              </select>
            </div>
            <button
              onClick={handleExport}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              <Download className="w-5 h-5" />
              Export
            </button>
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
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
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
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleViewDetails(teacher)}
                            className="p-1 text-blue-600 hover:bg-blue-50 rounded"
                            title="View Details"
                          >
                            <Eye className="w-5 h-5" />
                          </button>
                          <button
                            onClick={() => handleEdit(teacher)}
                            className="p-1 text-green-600 hover:bg-green-50 rounded"
                            title="Edit"
                          >
                            <Edit className="w-5 h-5" />
                          </button>
                          <button
                            onClick={() => handleDelete(teacher)}
                            className="p-1 text-red-600 hover:bg-red-50 rounded"
                            title="Delete"
                          >
                            <Trash2 className="w-5 h-5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Create/Edit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center p-6 border-b">
              <h2 className="text-2xl font-bold">{currentTeacher ? 'Edit Teacher' : 'Add New Teacher'}</h2>
              <button onClick={() => setShowModal(false)} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Teacher ID *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    value={formData.teacher_id}
                    onChange={(e) => setFormData({...formData, teacher_id: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email *</label>
                  <input
                    type="email"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">First Name *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    value={formData.first_name}
                    onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Last Name *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    value={formData.last_name}
                    onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                  <input
                    type="tel"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    value={formData.phone_number}
                    onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Department *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    value={formData.department}
                    onChange={(e) => setFormData({...formData, department: e.target.value})}
                    placeholder="e.g., Computer Science"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Specialization *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    value={formData.specialization}
                    onChange={(e) => setFormData({...formData, specialization: e.target.value})}
                    placeholder="e.g., Artificial Intelligence"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Qualification *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    value={formData.qualification}
                    onChange={(e) => setFormData({...formData, qualification: e.target.value})}
                    placeholder="e.g., PhD in Computer Science"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Experience (Years) *</label>
                  <input
                    type="number"
                    required
                    min="0"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    value={formData.experience_years}
                    onChange={(e) => setFormData({...formData, experience_years: e.target.value})}
                  />
                </div>
              </div>
              <div className="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                >
                  {currentTeacher ? 'Update' : 'Create'} Teacher
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Detail View Modal */}
      {showDetailModal && currentTeacher && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full">
            <div className="flex justify-between items-center p-6 border-b">
              <div className="flex items-center gap-3">
                <Award className="w-8 h-8 text-green-600" />
                <h2 className="text-2xl font-bold">Teacher Profile</h2>
              </div>
              <button onClick={() => setShowDetailModal(false)} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Teacher ID</p>
                  <p className="font-semibold">{currentTeacher.teacher_id}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Full Name</p>
                  <p className="font-semibold">{currentTeacher.full_name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Email</p>
                  <p className="font-semibold">{currentTeacher.email}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Phone</p>
                  <p className="font-semibold">{currentTeacher.phone_number || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Department</p>
                  <p className="font-semibold">{currentTeacher.department}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Specialization</p>
                  <p className="font-semibold">{currentTeacher.specialization}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Qualification</p>
                  <p className="font-semibold">{currentTeacher.qualification}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Experience</p>
                  <p className="font-semibold">{currentTeacher.experience_years} years</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Status</p>
                  <p className="font-semibold">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${currentTeacher.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {currentTeacher.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </Layout>
  )
}

export default TeachersEnhanced
