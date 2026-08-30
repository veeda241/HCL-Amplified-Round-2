// Re-export supabase client as `auth` for backward compatibility
// All components should migrate to importing from './supabase' directly
import { supabase } from './supabase';

// Supabase auth-compatible wrapper
export const auth = {
  get currentUser() {
    // This is a sync getter — Supabase requires async.
    // Components should use supabase.auth.getUser() instead.
    return null;
  },
};

export { supabase };
export default supabase;
