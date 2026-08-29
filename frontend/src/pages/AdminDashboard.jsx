import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { Shield, Users, GitBranch, Brain, LogOut, Moon, Sun, RefreshCw, Loader2 } from 'lucide-react'
import { useTheme } from '../contexts/ThemeContext'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const getAdminToken = () => {
  const session = JSON.parse(localStorage.getItem('admin_session') || 'null')
  return session?.token || null
}

const StatCard = ({ icon: Icon, label, value }) => (
  <div className="bg-white dark:bg-zinc-900 border border-gray-100 dark:border-zinc-800 rounded-2xl p-5 shadow-sm">
    <div className="flex items-center gap-3 mb-2">
      <div className="p-2 bg-gray-900 dark:bg-white rounded-xl">
        <Icon className="w-4 h-4 text-white dark:text-black" />
      </div>
      <p className="text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider">{label}</p>
    </div>
    <p className="text-3xl font-bold text-gray-900 dark:text-white">
      {value === null || value === undefined ? 'Not tracked' : value}
    </p>
  </div>
)

const AdminDashboard = () => {
  const [stats, setStats] = useState(null)
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()
  const { theme, toggleTheme } = useTheme()

  const loadData = useCallback(async () => {
    const token = getAdminToken()
    if (!token) {
      navigate('/admin/login')
      return
    }
    setLoading(true)
    setError(null)
    try {
      const headers = { Authorization: `Bearer ${token}` }
      const [statsRes, usersRes] = await Promise.all([
        axios.get(`${API_URL}/api/admin/stats`, { headers }),
        axios.get(`${API_URL}/api/admin/users`, { headers })
      ])
      setStats(statsRes.data)
      setUsers(usersRes.data.users || [])
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem('admin_session')
        navigate('/admin/login')
        return
      }
      setError(err.response?.data?.detail || err.message || 'Failed to load admin data')
    } finally {
      setLoading(false)
    }
  }, [navigate])

  useEffect(() => {
    loadData()
  }, [loadData])

  const handleLogout = () => {
    localStorage.removeItem('admin_session')
    navigate('/admin/login')
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-zinc-950 transition-colors duration-300">
      <header className="sticky top-4 sm:top-6 z-50 mx-auto w-[92%] sm:w-[95%] max-w-6xl rounded-2xl border bg-white/80 dark:bg-zinc-900/80 backdrop-blur-xl border-gray-200 dark:border-zinc-800 shadow-sm">
        <nav className="flex items-center justify-between p-2 px-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-red-600 rounded-xl">
              <Shield className="w-4 h-4 text-white" />
            </div>
            <p className="text-sm font-bold tracking-tight text-gray-900 dark:text-white">SkillRoute Admin</p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={loadData}
              disabled={loading}
              className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-zinc-800 disabled:opacity-50"
              aria-label="Refresh"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-zinc-800"
              aria-label="Toggle dark mode"
            >
              {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
            <button
              onClick={handleLogout}
              className="p-2 rounded-lg text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
              aria-label="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </nav>
      </header>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-1">Platform Overview</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-8">Stats and student roster for SkillRoute</p>

        {loading && !stats ? (
          <div className="flex items-center justify-center py-24">
            <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
          </div>
        ) : error ? (
          <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 rounded-xl p-4 text-sm font-medium">
            {error}
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
              <StatCard icon={Users} label="Total Students" value={stats?.total_users} />
              <StatCard icon={GitBranch} label="Active Roadmaps" value={stats?.total_roadmaps} />
              <StatCard icon={Brain} label="Quizzes Taken" value={stats?.total_quizzes} />
            </div>

            <div className="bg-white dark:bg-zinc-900 border border-gray-100 dark:border-zinc-800 rounded-2xl overflow-hidden shadow-sm">
              <div className="px-5 py-4 border-b border-gray-100 dark:border-zinc-800">
                <h2 className="text-sm font-bold text-gray-900 dark:text-white">Students ({users.length})</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider border-b border-gray-100 dark:border-zinc-800">
                      <th className="px-5 py-3">Name</th>
                      <th className="px-5 py-3">Education</th>
                      <th className="px-5 py-3">Goals</th>
                      <th className="px-5 py-3">Skills</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.length === 0 ? (
                      <tr>
                        <td colSpan={4} className="px-5 py-8 text-center text-gray-400 dark:text-gray-500">
                          No students yet
                        </td>
                      </tr>
                    ) : (
                      users.map((u) => (
                        <tr key={u.id} className="border-b border-gray-50 dark:border-zinc-800/50 last:border-0">
                          <td className="px-5 py-3 font-medium text-gray-900 dark:text-white">{u.name || '—'}</td>
                          <td className="px-5 py-3 text-gray-600 dark:text-gray-400">{u.education || '—'}</td>
                          <td className="px-5 py-3 text-gray-600 dark:text-gray-400 max-w-xs truncate">{u.goals || '—'}</td>
                          <td className="px-5 py-3 text-gray-600 dark:text-gray-400 max-w-xs truncate">{u.skills || '—'}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  )
}

export default AdminDashboard
