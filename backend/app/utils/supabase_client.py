import os
from supabase import create_client, Client

_admin_client: Client = None
_anon_client: Client = None


def _get_env():
    url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    return url, anon_key, service_key


def get_admin_client() -> Client:
    """Service-role client for privileged server-side DB access (bypasses RLS)."""
    global _admin_client
    if _admin_client is None:
        url, _, service_key = _get_env()
        if not url or not service_key:
            raise RuntimeError("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not configured")
        _admin_client = create_client(url, service_key)
    return _admin_client


def get_anon_client() -> Client:
    """Anon-key client, used to verify user access tokens via the Auth API."""
    global _anon_client
    if _anon_client is None:
        url, anon_key, _ = _get_env()
        if not url or not anon_key:
            raise RuntimeError("SUPABASE_URL / SUPABASE_ANON_KEY not configured")
        _anon_client = create_client(url, anon_key)
    return _anon_client
