import { useState, useEffect, useRef, useCallback } from 'react'
import { useToast } from '../contexts/ToastContext'
import axios from 'axios'
import { Bot } from 'lucide-react'
import { useSupabaseRealtime } from './useSupabaseRealtime'
import { supabase } from '../supabase'

export const useDashboardData = () => {
    const [profile, setProfile] = useState(null)
    const [roadmap, setRoadmap] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [isGenerating, setIsGenerating] = useState(false)
    const [generationMode, setGenerationMode] = useState(null)
    const [supabaseUserId, setSupabaseUserId] = useState(null)

    const autoAdaptShown = useRef(false)
    const toast = useToast()

    const API_URL = import.meta.env.VITE_API_URL || ''

    const getToken = async () => {
        const adminSession = JSON.parse(localStorage.getItem('admin_session') || 'null')
        if (adminSession && adminSession.token) {
            return adminSession.token
        }
        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (session?.access_token) {
                return session.access_token
            }
        } catch {
            // Supabase not configured or not logged in
        }
        return null
    }

    // Resolve the Supabase user ID for realtime subscriptions
    useEffect(() => {
        const resolveUser = async () => {
            // Admin sessions don't have a Supabase user ID — skip realtime
            const adminSession = JSON.parse(localStorage.getItem('admin_session') || 'null')
            if (adminSession?.token) {
                setSupabaseUserId(null)
                return
            }
            const { data: { user } } = await supabase.auth.getUser()
            setSupabaseUserId(user?.id || null)
        }
        resolveUser()
    }, [])

    const loadProfile = useCallback(async (signal) => {
        try {
            const token = await getToken()
            const headers = token ? { Authorization: `Bearer ${token}` } : {}
            const response = await axios.get(`${API_URL}/api/students/profile`, {
                headers,
                signal
            })
            if (response.data && !response.data.message) {
                setProfile(response.data)
            }
        } catch (err) {
            if (err.name !== 'CanceledError' && err.code !== 'ECONNABORTED') {
                console.error('Profile load error:', err)
                setError(prev => ({ ...prev, profile: err.message }))
            }
        }
    }, [API_URL])

    const loadRoadmap = useCallback(async (signal) => {
        try {
            const token = await getToken()
            const headers = token ? { Authorization: `Bearer ${token}` } : {}
            const response = await axios.get(`${API_URL}/api/career/roadmap`, {
                headers,
                signal
            })

            if (response.data && !response.data.message) {
                setRoadmap(response.data)

                // Auto-adapt detection
                if (response.data.needs_adaptation && !autoAdaptShown.current) {
                    autoAdaptShown.current = true
                    toast.info({
                        title: (
                            <div className="flex items-center gap-2">
                                <Bot className="w-4 h-4" />
                                <span>Agent Suggestion</span>
                            </div>
                        ),
                        description: response.data.adaptation_reason || 'Your progress seems stalled. Want the agent to adapt your roadmap?',
                        action: {
                            label: 'Adapt Now',
                            onClick: () => window.dispatchEvent(new CustomEvent('triggerAdapt'))
                        }
                    })
                }
            } else {
                setRoadmap(null)
            }
        } catch (err) {
            if (err.name !== 'CanceledError' && err.code !== 'ECONNABORTED') {
                // If 404, it might just mean no roadmap exists yet, which is fine
                if (err.response && err.response.status === 404) {
                    setRoadmap(null)
                } else {
                    console.error('Roadmap load error:', err)
                    setError(prev => ({ ...prev, roadmap: err.message }))
                }
            }
        }
    }, [API_URL, toast])

    // ── Realtime handlers ────────────────────────────────────────
    // When Supabase broadcasts a roadmap change, update local state
    // immediately — no polling, no manual refresh needed.
    const handleRealtimeUpdate = useCallback((row) => {
        if (!row) return

        // Build the shape that the dashboard expects
        const updatedRoadmap = {
            career_decision: row.career_decision,
            learning_roadmap: row.learning_roadmap,
            progress: row.progress,
            updated_at: row.updated_at,
        }

        setRoadmap((prev) => {
            // Avoid no-op re-renders
            if (prev?.updated_at === row.updated_at) return prev
            return updatedRoadmap
        })
    }, [])

    const handleRealtimeDelete = useCallback(() => {
        setRoadmap(null)
        toast.success('Roadmap has been reset.')
    }, [toast])

    // Subscribe to Supabase Realtime (no-op for admin sessions)
    useSupabaseRealtime(supabaseUserId, handleRealtimeUpdate, handleRealtimeDelete)

    const generateRoadmap = async () => {
        if (!profile) return false

        setLoading(true)
        setIsGenerating(true)
        setGenerationMode('generate')
        try {
            const token = await getToken()
            const headers = token ? { Authorization: `Bearer ${token}` } : {}
            const response = await axios.post(`${API_URL}/api/career/roadmap`, profile, {
                headers
            })
            setRoadmap(response.data)
            toast.success('Roadmap generated successfully!')
            return true
        } catch (err) {
            const errorMsg = err.response?.data?.detail || err.message || 'An error occurred'
            toast.error(`Failed to generate roadmap: ${errorMsg}`)
            return false
        } finally {
            setLoading(false)
            setIsGenerating(false)
            setGenerationMode(null)
        }
    }

    const adaptRoadmap = async () => {
        setLoading(true)
        setIsGenerating(true)
        setGenerationMode('adapt')
        try {
            const token = await getToken()
            const headers = token ? { Authorization: `Bearer ${token}` } : {}
            await axios.post(`${API_URL}/api/progress/adapt`, {}, {
                headers
            })
            // Realtime will handle the state update, but also
            // do a manual fetch as a safety net
            await loadRoadmap()
            toast.success({
                title: 'Roadmap Adapted',
                description: 'Your learning path has been updated based on your recent progress.'
            })
            return true
        } catch (err) {
            toast.error('Failed to adapt roadmap. Please try again.')
            return false
        } finally {
            setLoading(false)
            setIsGenerating(false)
            setGenerationMode(null)
        }
    }

    const resetCareerPath = async () => {
        setLoading(true)
        try {
            const token = await getToken()
            const headers = token ? { Authorization: `Bearer ${token}` } : {}
            await axios.delete(`${API_URL}/api/career/roadmap`, {
                headers
            })
            // Realtime will handle the DELETE event, but also
            // clear immediately for instant feedback
            setRoadmap(null)
            toast.success('Career path reset successfully!')
            return true
        } catch (err) {
            toast.error('Failed to reset career path.')
            return false
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        const controller = new AbortController()
        setLoading(true)

        Promise.all([
            loadProfile(controller.signal),
            loadRoadmap(controller.signal)
        ]).finally(() => {
            setLoading(false)
        })

        return () => controller.abort()
    }, [loadProfile, loadRoadmap])

    const refreshData = async () => {
        setLoading(true)
        await Promise.all([loadProfile(), loadRoadmap()])
        setLoading(false)
    }

    return {
        profile,
        roadmap,
        loading,
        error,
        isGenerating,
        generationMode,
        generateRoadmap,
        adaptRoadmap,
        resetCareerPath,
        refreshData
    }
}
