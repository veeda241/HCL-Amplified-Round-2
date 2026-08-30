import { useState } from 'react';
import { Eye, EyeOff, Compass, Moon, Sun } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './card';
import { Input } from './input';
import { Button } from './button';
import { Label } from './label';
import { useTheme } from '../../contexts/ThemeContext';
import axios from 'axios';

export const SignIn = ({ onLogin }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const handleSignIn = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const API_URL = import.meta.env.VITE_API_URL || '';
      const adminRes = await axios.post(`${API_URL}/api/admin/login`, {
        email,
        password
      });

      if (adminRes.data.success) {
        localStorage.setItem('admin_session', JSON.stringify({
          email: adminRes.data.admin_email,
          token: adminRes.data.token,
          timestamp: Date.now()
        }));
        if (onLogin) onLogin();
        navigate('/dashboard');
        return;
      }
    } catch (err) {
      if (err?.response?.status === 401) {
        setError('Invalid email or password. Try admin@skillroute.com / admin123');
      } else if (err?.code === 'ERR_NETWORK') {
        setError('Cannot connect to server. Make sure the backend is running on port 8000.');
      } else {
        setError('Login failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center font-sans w-full bg-gray-50 dark:bg-black p-4 sm:p-6 lg:p-8 relative">
      <button
        onClick={toggleTheme}
        className="fixed top-6 right-6 z-[9999] p-3 rounded-full bg-white dark:bg-zinc-800 text-gray-900 dark:text-white border-2 border-gray-300 dark:border-zinc-600 shadow-2xl hover:scale-110 transition-all duration-200"
        aria-label="Toggle dark mode"
        title="Toggle dark mode"
      >
        {theme === 'dark' ? (
          <Sun className="h-6 w-6 text-yellow-400" />
        ) : (
          <Moon className="h-6 w-6 text-indigo-600" />
        )}
      </button>

      <div className="mb-6 sm:mb-8 text-center animate-fade-in">
        <div className="flex items-center justify-center gap-3 mb-2">
          <div className="p-2.5 bg-white dark:bg-zinc-900 rounded-xl shadow-sm border border-gray-200 dark:border-zinc-800">
            <Compass className="w-6 h-6 sm:w-8 h-8 text-black dark:text-white" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white tracking-tight">SkillRoute</h1>
        </div>
        <p className="text-gray-500 dark:text-gray-400 text-xs sm:text-sm font-medium">Your personalized learning journey</p>
      </div>

      <Card className="w-full max-w-md shadow-xl border-2 border-gray-200 dark:border-zinc-700 bg-white dark:bg-zinc-900">
        <CardHeader className="space-y-1 text-center pb-2">
          <CardTitle className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Welcome back</CardTitle>
          <CardDescription className="text-gray-500 dark:text-gray-300 font-medium">
            Enter your credentials to access your account
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && (
            <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 rounded-lg p-3 text-sm font-medium">
              {error}
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSignIn}>
            <div className="space-y-2">
              <Label htmlFor="email" className="dark:text-gray-200">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="bg-white dark:bg-zinc-800 border-gray-200 dark:border-zinc-700 dark:text-white dark:placeholder-gray-400 focus:border-black dark:focus:border-indigo-500 focus:ring-black dark:focus:ring-indigo-500"
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
                  className="bg-white dark:bg-zinc-800 border-gray-200 dark:border-zinc-700 dark:text-white dark:placeholder-gray-400 focus:border-black dark:focus:border-indigo-500 focus:ring-black dark:focus:ring-indigo-500 pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-black dark:text-gray-400 dark:hover:text-white"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
            <Button
              type="submit"
              className="w-full bg-black hover:bg-gray-800 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white shadow-md"
              disabled={loading}
            >
              {loading ? 'Signing In...' : 'Sign In'}
            </Button>
          </form>

          <div className="text-center text-xs text-gray-400 dark:text-gray-500 mt-2">
            Default: admin@skillroute.com / admin123
          </div>
        </CardContent>
      </Card>

    </div>
  );
};

export default SignIn;
