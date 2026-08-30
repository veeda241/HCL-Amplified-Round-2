import { useEffect, useRef, useCallback } from 'react'
import { supabase } from '../supabase'

/**
 * Subscribes to Supabase Realtime changes on the `roadmaps` table
 * filtered to the current user's row. When an UPDATE arrives, the
 * callback receives the fresh row so the dashboard can re-render
 * without polling.
 *
 * Real-time only works when the user authenticated via Supabase Auth
 * (not the admin session). For admin sessions this is a no-op.
 *
 * @param {string|null} userId   - The Supabase auth user ID (from session.user.id)
 * @param {function}    onUpdate - Called with the new roadmap row on UPDATE events
 * @param {function}    onDelete - Called when the roadmap row is DELETEd (e.g. reset)
 */
export function useSupabaseRealtime(userId, onUpdate, onDelete) {
  const channelRef = useRef(null)
  const onUpdateRef = useRef(onUpdate)
  const onDeleteRef = useRef(onDelete)

  // Keep refs fresh without re-subscribing
  useEffect(() => {
    onUpdateRef.current = onUpdate
  }, [onUpdate])

  useEffect(() => {
    onDeleteRef.current = onDelete
  }, [onDelete])

  useEffect(() => {
    // Don't subscribe without a valid Supabase user ID
    if (!userId) return

    // Clean up any previous subscription
    if (channelRef.current) {
      supabase.removeChannel(channelRef.current)
      channelRef.current = null
    }

    const channel = supabase
      .channel(`roadmap:${userId}`)
      .on(
        'postgres_changes',
        {
          event: 'UPDATE',   // We care about progress updates
          schema: 'public',
          table: 'roadmaps',
          filter: `user_id=eq.${userId}`,
        },
        (payload) => {
          console.log('[Realtime] Roadmap updated:', payload.new?.updated_at)
          onUpdateRef.current?.(payload.new)
        }
      )
      .on(
        'postgres_changes',
        {
          event: 'DELETE',   // Roadmap reset
          schema: 'public',
          table: 'roadmaps',
          filter: `user_id=eq.${userId}`,
        },
        (payload) => {
          console.log('[Realtime] Roadmap deleted')
          onDeleteRef.current?.()
        }
      )
      .on(
        'postgres_changes',
        {
          event: 'INSERT',   // New roadmap generated
          schema: 'public',
          table: 'roadmaps',
          filter: `user_id=eq.${userId}`,
        },
        (payload) => {
          console.log('[Realtime] Roadmap created:', payload.new?.updated_at)
          onUpdateRef.current?.(payload.new)
        }
      )
      .subscribe((status) => {
        if (status === 'SUBSCRIBED') {
          console.log(`[Realtime] Subscribed to roadmap changes for user ${userId}`)
        } else if (status === 'CHANNEL_ERROR') {
          console.warn('[Realtime] Subscription failed — will use manual refresh')
        }
      })

    channelRef.current = channel

    return () => {
      if (channelRef.current) {
        supabase.removeChannel(channelRef.current)
        channelRef.current = null
      }
    }
  }, [userId])

  return {
    /** Force re-subscribe (e.g. after re-login) */
    resubscribe: useCallback(() => {
      if (channelRef.current) {
        supabase.removeChannel(channelRef.current)
        channelRef.current = null
      }
      // The effect above will re-run if userId changes
    }, []),
  }
}
