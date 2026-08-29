import { useState } from 'react';
import { Eye, EyeOff, Shield, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './card';
import { Input } from './input';
import { Button } from './button';
import { Label } from './label';
import { useTheme } from '../../contexts/ThemeContext';
import axios from 'axios';

const AdminLogin = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { theme } = useTheme();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      const response = await axios.post(`${API_URL}/api/admin/login`, {
        email,
        password
      });

      if (response.data.success) {
        // Store admin session with token
        localStorage.setItem('admin_session', JSON.stringify({
          email: response.data.admin_email,
          token: response.data.token,
          timestamp: Date.now()
        }));
        // Full reload so App re-reads the just-written admin session from localStorage
        // (React Router navigation alone wouldn't refresh App's adminUser state on this tab)
        window.location.href = '/admin/dashboard';
      }
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Invalid admin credentials');
      } else {
        setError(err.message || 'Failed to login. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleBackToLogin = () => {
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center font-sans w-full bg-gray-50 dark:bg-black p-4 sm:p-6 lg:p-8 relative">
      {/* Back Button */}
      <button
        onClick={handleBackToLogin}
        className="fixed top-6 left-6 z-[9999] p-3 rounded-full bg-white dark:bg-zinc-800 text-gray-900 dark:text-white border-2 border-gray-300 dark:border-zinc-600 shadow-2xl hover:scale-110 transition-all duration-200"
        aria-label="Back to login"
        title="Back to login"
      >
        <ArrowLeft className="h-6 w-6" />
      </button>

      <div className="mb-6 sm:mb-8 text-center animate-fade-in">
        <div className="flex items-center justify-center gap-3 mb-2">
          <div className="p-2.5 bg-red-600 rounded-xl shadow-sm">
            <Shield className="w-6 h-6 sm:w-8 sm:h-8 text-white" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white tracking-tight">Admin Portal</h1>
        </div>
        <p className="text-gray-500 dark:text-gray-400 text-xs sm:text-sm font-medium">SkillRoute Administration</p>
      </div>

      <Card className="w-full max-w-md shadow-xl border-2 border-gray-200 dark:border-zinc-700 bg-white dark:bg-zinc-900">
        <CardHeader className="space-y-1 text-center pb-2">
          <CardTitle className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Admin Login</CardTitle>
          <CardDescription className="text-gray-500 dark:text-gray-300 font-medium">
            Enter your admin credentials to access the dashboard
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && (
            <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 rounded-lg p-3 text-sm font-medium">
              {error}
            </div>
          )}

          <form className="space-y-4" onSubmit={handleLogin}>
            <div className="space-y-2">
              <Label htmlFor="email" className="dark:text-gray-200">Admin Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="admin@skillroute.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="bg-white dark:bg-zinc-800 border-gray-200 dark:border-zinc-700 dark:text-white dark:placeholder-gray-400 focus:border-red-600 dark:focus:border-red-500 focus:ring-red-600 dark:focus:ring-red-500"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="dark:text-gray-200">Password</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="bg-white dark:bg-zinc-800 border-gray-200 dark:border-zinc-700 dark:text-white dark:placeholder-gray-400 focus:border-red-600 dark:focus:border-red-500 focus:ring-red-600 dark:focus:ring-red-500 pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
            <Button
              type="submit"
              className="w-full bg-red-600 hover:bg-red-700 text-white shadow-md"
              disabled={loading}
            >
              {loading ? 'Signing In...' : 'Admin Sign In'}
            </Button>
          </form>

          <div className="text-center text-sm text-gray-500 dark:text-gray-400 font-medium mt-4">
            <button 
              onClick={handleBackToLogin} 
              className="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 font-bold hover:underline"
            >
              Back to Student Login
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Security Notice */}
      <div className="mt-6 text-center max-w-md">
        <p className="text-xs text-gray-400 dark:text-gray-500">
          🔒 This area is restricted to authorized administrators only.
          All actions are logged and monitored.
        </p>
      </div>
    </div>
  );
};

export default AdminLogin;
