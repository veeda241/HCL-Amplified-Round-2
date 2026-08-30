import jwt
from jwt import PyJWKClient
import hashlib
import time
import os
import json
import requests
from fastapi import Header, HTTPException

# ---------- Admin session store (persisted to disk) ----------
_admin_sessions: dict = {}
_SESSIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "admin_sessions.json")

ADMIN_USER_ID = "admin_user"  # Special UID returned for admin sessions

# Supabase JWKS URL for verifying tokens (preferred over static secret)
SUPABASE_JWKS_URL = os.getenv("SUPABASE_JWKS_URL", "")
# Fallback: static JWT secret (for environments where JWKS isn't available)
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")

# Cache the JWKS keys
_jwks_cache = None
_jwks_cache_time = 0
_JWKS_CACHE_TTL = 3600  # 1 hour


def _load_sessions():
    """Load admin sessions from disk."""
    global _admin_sessions
    try:
        if os.path.exists(_SESSIONS_FILE):
            with open(_SESSIONS_FILE, "r") as f:
                _admin_sessions = json.load(f)
    except (json.JSONDecodeError, IOError):
        _admin_sessions = {}


def _save_sessions():
    """Persist admin sessions to disk."""
    try:
        with open(_SESSIONS_FILE, "w") as f:
            json.dump(_admin_sessions, f)
    except IOError:
        pass


# Load sessions on module import
_load_sessions()


def create_admin_session(email: str) -> str:
    """Create a simple session token for admin."""
    token = hashlib.sha256(
        f"{email}:{time.time()}:{os.urandom(16).hex()}".encode()
    ).hexdigest()
    _admin_sessions[token] = {"email": email, "created_at": time.time()}
    _save_sessions()
    return token


def verify_admin_session_token(token: str) -> bool:
    """Return True if token is a valid admin session."""
    session = _admin_sessions.get(token)
    if not session:
        return False
    if time.time() - session["created_at"] > 86400:
        del _admin_sessions[token]
        _save_sessions()
        return False
    return True


def _get_jwks():
    """Fetch and cache JWKS keys from Supabase."""
    global _jwks_cache, _jwks_cache_time

    now = time.time()
    if _jwks_cache and (now - _jwks_cache_time) < _JWKS_CACHE_TTL:
        return _jwks_cache

    if not SUPABASE_JWKS_URL:
        return None

    try:
        resp = requests.get(SUPABASE_JWKS_URL, timeout=10)
        resp.raise_for_status()
        jwks = resp.json()
        _jwks_cache = jwks
        _jwks_cache_time = now
        return jwks
    except Exception as e:
        print(f"WARNING: Failed to fetch JWKS: {e}")
        return _jwks_cache  # Return stale cache if available


def _verify_supabase_token(token: str) -> str:
    """Verify a Supabase JWT using JWKS and return the user ID (sub claim).

    Tries JWKS verification first (more secure, uses public keys).
    Falls back to static secret if JWKS URL is not configured.
    """
    # Try JWKS-based verification first
    jwks = _get_jwks()
    if jwks:
        try:
            # Get the signing key from JWKS
            signing_key = PyJWKClient(
                SUPABASE_JWKS_URL,
                cache_jwk_set=True,
                cache_keys=True,
            )
            public_key = signing_key.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                public_key.key,
                algorithms=["RS256", "HS256"],
                audience="authenticated",
                options={"verify_aud": True},
            )
            return payload.get("sub", "")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError as e:
            print(f"WARNING: JWKS verification failed, trying static secret: {e}")
        except Exception as e:
            print(f"WARNING: JWKS client error, trying static secret: {e}")

    # Fallback to static secret verification
    if not SUPABASE_JWT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="No JWT verification method configured. Set SUPABASE_JWKS_URL or SUPABASE_JWT_SECRET."
        )

    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256", "RS256"],
            audience="authenticated",
        )
        return payload.get("sub", "")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


# ---------- Unified token verifier ----------

def verify_token(authorization: str = Header(...)) -> str:
    """Accept either a Supabase JWT token or an admin session token.

    Returns a user-id string:
      - Supabase user ID (sub) for Supabase tokens
      - ADMIN_USER_ID ("admin_user") for admin session tokens
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.split(" ")[1]

    # 1. Check admin session first
    if verify_admin_session_token(token):
        return ADMIN_USER_ID

    # 2. Fall back to Supabase JWT verification (JWKS or static secret)
    return _verify_supabase_token(token)


# Keep the old name so existing imports don't break
verify_firebase_token = verify_token


def get_optional_user(authorization: str = Header(None)) -> str:
    """Like verify_token but returns a default user when no token is provided.

    Use this dependency on routes that should work without authentication:
    if a valid token is present, use it; otherwise fall back to a demo user.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return "demo_user"

    token = authorization.split(" ")[1]

    # 1. Check admin session
    if verify_admin_session_token(token):
        return ADMIN_USER_ID

    # 2. Try Supabase JWT verification
    try:
        return _verify_supabase_token(token)
    except HTTPException:
        return "demo_user"
