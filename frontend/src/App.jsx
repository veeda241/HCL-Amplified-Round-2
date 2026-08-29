import { Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect, lazy, Suspense } from 'react'

const SignIn = lazy(() => import('./components/ui/SignIn'))
const SignUp = lazy(() => import('./components/ui/SignUp'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Profile = lazy(() => import('./pages/Profile'))
const ProfileSetup = lazy(() => import('./components/ProfileSetup'))
const AdminLogin = lazy(() => import('./components/ui/AdminLogin'))
const AdminDashboard = lazy(() => import('./pages/AdminDashboard'))

const LoadingScreen = () => (
  <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-black">
    <div className="flex flex-col items-center gap-4">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black dark:border-white"></div>
      <p className="text-gray-500 dark:text-gray-400 font-medium">Loading...</p>
    </div>
  </div>
)

function isAdminLoggedIn() {
  try {
    const session = JSON.parse(localStorage.getItem('admin_session'))
    return session && session.token && session.email
  } catch {
    return false
  }
}

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [adminUser, setAdminUser] = useState(isAdminLoggedIn())

  useEffect(() => {
    // Check for admin session from other tabs
    const handleStorage = () => setAdminUser(isAdminLoggedIn())
    window.addEventListener('storage', handleStorage)
    return () => window.removeEventListener('storage', handleStorage)
  }, [])

  useEffect(() => {
    let subscription = null
    let cancelled = false

    import('./supabaseClient')
      .then(({ supabase }) => {
        if (cancelled) return

        supabase.auth.getSession().then(({ data: { session } }) => {
          if (!cancelled) {
            setUser(session?.user ?? null)
            setLoading(false)
          }
        })

        const { data } = supabase.auth.onAuthStateChange((_event, session) => {
          if (!cancelled) {
            setUser(session?.user ?? null)
            setLoading(false)
          }
        })
        subscription = data.subscription
      })
      .catch(() => {
        // Supabase not configured — app still works for admin routes
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
      if (subscription) subscription.unsubscribe()
    }
  }, [])

  if (loading) {
    return <LoadingScreen />
  }

  return (
    <Suspense fallback={<LoadingScreen />}>
      <Routes>
        {/* Admin routes — no Supabase dependency */}
        <Route path="/admin/login" element={adminUser ? <Navigate to="/admin/dashboard" /> : <AdminLogin />} />
        <Route path="/admin/dashboard" element={adminUser ? <AdminDashboard /> : <Navigate to="/admin/login" />} />

        {/* Student routes — require Supabase auth (admins are routed to /admin/dashboard instead) */}
        <Route
          path="/login"
          element={adminUser ? <Navigate to="/admin/dashboard" /> : user ? <Navigate to="/dashboard" /> : <SignIn />}
        />
        <Route
          path="/signup"
          element={adminUser ? <Navigate to="/admin/dashboard" /> : user ? <Navigate to="/dashboard" /> : <SignUp />}
        />
        <Route
          path="/profile-setup"
          element={adminUser ? <Navigate to="/admin/dashboard" /> : user ? <ProfileSetup /> : <Navigate to="/login" />}
        />
        <Route
          path="/profile"
          element={adminUser ? <Navigate to="/admin/dashboard" /> : user ? <Profile /> : <Navigate to="/login" />}
        />
        <Route
          path="/dashboard"
          element={adminUser ? <Navigate to="/admin/dashboard" /> : user ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route
          path="/"
          element={<Navigate to={adminUser ? "/admin/dashboard" : user ? "/dashboard" : "/login"} />}
        />
      </Routes>
    </Suspense>
  )
}

export default App
