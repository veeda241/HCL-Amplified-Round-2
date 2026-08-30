import { Routes, Route, Navigate } from 'react-router-dom'
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const Profile = lazy(() => import('./pages/Profile'))
const ProfileSetup = lazy(() => import('./components/ProfileSetup'))

const LoadingScreen = () => (
  <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-black">
    <div className="flex flex-col items-center gap-4">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black dark:border-white"></div>
      <p className="text-gray-500 dark:text-gray-400 font-medium">Loading...</p>
    </div>
  </div>
)

function App() {
  return (
    <Suspense fallback={<LoadingScreen />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile-setup" element={<ProfileSetup />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Suspense>
  )
}

export default App
