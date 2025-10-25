import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import api from '../utils/api'
import { Search, Plus, Edit, Trash2, X, Eye, UserPlus, Filter, Download } from 'lucide-react'

const StudentsEnhanced = () => {
  const [students, setStudents] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterGrade, setFilterGrade] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [showDetailModal, setShowDetailModal] = useState(false)
  const [currentStudent, setCurrentStudent] = useState(null)
  const [formData, setFormData] = useState({
    student_id: '',
    email: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    date_of_birth: '',
    gender: 'M',
    grade: '',
    address: '',
    gpa: ''
  })

  useEffect(() => {
    fetchStudents()
  }, [])

  const fetchStudents = async () => {
    try {
      const response = await api.get('/students/')
      setStudents(response.data.data || response.data.results || [])
    } catch (error) {
      alert('Failed to fetch students')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setCurrentStudent(null)
    setFormData({
      student_id: '',
      email: '',
      first_name: '',
      last_name: '',
      phone_number: '',
      date_of_birth: '',
      gender: 'M',
      grade: '',
      address: '',
      gpa: ''
    })
    setShowModal(true)
  }

  const handleEdit = (student) => {
    setCurrentStudent(student)
    setFormData({
      student_id: student.student_id || '',
      email: student.email || '',
      first_name: student.first_name || '',
      last_name: student.last_name || '',
      phone_number: student.phone_number || '',
      date_of_birth: student.date_of_birth || '',
      gender: student.gender || 'M',
      grade: student.grade || '',
      address: student.address || '',
      gpa: student.gpa || ''
    })
    setShowModal(true)
  }

  const handleViewDetails = (student) => {
    setCurrentStudent(student)
    setShowDetailModal(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (currentStudent) {
        // Update existing student
        await api.put(`/students/${currentStudent.id}/`, formData)
        alert('Student updated successfully!')
      } else {
        // Create new student
        await api.post('/students/', formData)
        alert('Student created successfully!')
      }
      setShowModal(false)
      fetchStudents()
    } catch (error) {
      alert(error.response?.data?.error?.message || 'Failed to save student')
    }
  }

  const handleDelete = async (student) => {
    if (!confirm(`Are you sure you want to delete ${student.full_name}?`)) return
    
    try {
      await api.delete(`/students/${student.id}/`)
      alert('Student deleted successfully!')
      fetchStudents()
    } catch (error) {
      alert('Failed to delete student')
    }
  }

  const handleExport = () => {
    const csv = [
      ['Student ID', 'Name', 'Email', 'Grade', 'GPA', 'Status'],
      ...filteredStudents.map(s => [
        s.student_id,
        s.full_name,
        s.email,
        s.grade,
        s.gpa,
        s.is_active ? 'Active' : 'Inactive'
      ])
    ].map(row => row.join(',')).join('\n')
    
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'students.csv'
    a.click()
  }

  const filteredStudents = students.filter(student => {
    const matchesSearch = student.student_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.email?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesGrade = !filterGrade || student.grade?.toString() === filterGrade
    return matchesSearch && matchesGrade
  })

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Students Management</h1>
            <p className="text-gray-600 mt-2">Manage student records and information</p>
          </div>
          <button
            onClick={handleCreate}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            <UserPlus className="w-5 h-5" />
            Add Student
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex flex-wrap items-center gap-4 mb-6">
            <div className="flex-1 min-w-[200px] relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search students..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="flex items-center gap-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <select
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                value={filterGrade}
                onChange={(e) => setFilterGrade(e.target.value)}
              >
                <option value="">All Grades</option>
                <option value="9">Grade 9</option>
                <option value="10">Grade 10</option>
                <option value="11">Grade 11</option>
                <option value="12">Grade 12</option>
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
            <div className="text-center py-12 text-gray-500">Loading students...</div>
          ) : filteredStudents.length === 0 ? (
            <div className="text-center py-12 text-gray-500">No students found</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Grade</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">GPA</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {filteredStudents.map((student) => (
                    <tr key={student.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{student.student_id}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{student.full_name}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{student.email}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">Grade {student.grade}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{student.gpa || 'N/A'}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${student.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                          {student.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleViewDetails(student)}
                            className="p-1 text-blue-600 hover:bg-blue-50 rounded"
                            title="View Details"
                          >
                            <Eye className="w-5 h-5" />
                          </button>
                          <button
                            onClick={() => handleEdit(student)}
                            className="p-1 text-green-600 hover:bg-green-50 rounded"
                            title="Edit"
                          >
                            <Edit className="w-5 h-5" />
                          </button>
                          <button
                            onClick={() => handleDelete(student)}
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
              <h2 className="text-2xl font-bold">{currentStudent ? 'Edit Student' : 'Add New Student'}</h2>
              <button onClick={() => setShowModal(false)} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Student ID *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    value={formData.student_id}
                    onChange={(e) => setFormData({...formData, student_id: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email *</label>
                  <input
                    type="email"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">First Name *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    value={formData.first_name}
                    onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Last Name *</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    value={formData.last_name}
                    onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                  <input
                    type="tel"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    value={formData.phone_number}
                    onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
                  <input
                    type="date"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    value={formData.date_of_birth}
                    onChange={(e) => setFormData({...formData, date_of_birth: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
                  <select
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    value={formData.gender}
                    onChange={(e) => setFormData({...formData, gender: e.target.value})}
                  >
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                    <option value="O">Other</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Grade *</label>
                  <select
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    value={formData.grade}
                    onChange={(e) => setFormData({...formData, grade: e.target.value})}
                  >
                    <option value="">Select Grade</option>
                    <option value="9">Grade 9</option>
                    <option value="10">Grade 10</option>
                    <option value="11">Grade 11</option>
                    <option value="12">Grade 12</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">GPA</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    max="4.0"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    value={formData.gpa}
                    onChange={(e) => setFormData({...formData, gpa: e.target.value})}
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                  <textarea
                    rows="2"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    value={formData.address}
                    onChange={(e) => setFormData({...formData, address: e.target.value})}
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
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {currentStudent ? 'Update' : 'Create'} Student
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Detail View Modal */}
      {showDetailModal && currentStudent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full">
            <div className="flex justify-between items-center p-6 border-b">
              <h2 className="text-2xl font-bold">Student Details</h2>
              <button onClick={() => setShowDetailModal(false)} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Student ID</p>
                  <p className="font-semibold">{currentStudent.student_id}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Full Name</p>
                  <p className="font-semibold">{currentStudent.full_name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Email</p>
                  <p className="font-semibold">{currentStudent.email}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Phone</p>
                  <p className="font-semibold">{currentStudent.phone_number || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Grade</p>
                  <p className="font-semibold">Grade {currentStudent.grade}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">GPA</p>
                  <p className="font-semibold">{currentStudent.gpa || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Date of Birth</p>
                  <p className="font-semibold">{currentStudent.date_of_birth || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Gender</p>
                  <p className="font-semibold">{currentStudent.gender === 'M' ? 'Male' : currentStudent.gender === 'F' ? 'Female' : 'Other'}</p>
                </div>
                <div className="col-span-2">
                  <p className="text-sm text-gray-500">Address</p>
                  <p className="font-semibold">{currentStudent.address || 'N/A'}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </Layout>
  )
}

export default StudentsEnhanced
