from firebase_admin import auth
from fastapi import Header, HTTPException
import hashlib
import time
import os
import json

# ---------- Admin session store (persisted to disk) ----------
_admin_sessions: dict = {}
_SESSIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "admin_sessions.json")

ADMIN_USER_ID = "admin_user"  # Special UID returned for admin sessions


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


# ---------- Unified token verifier ----------

def verify_token(authorization: str = Header(...)) -> str:
    """Accept either a Firebase ID token or an admin session token.

    Returns a user-id string:
      - Firebase UID for Firebase tokens
      - ADMIN_USER_ID ("admin_user") for admin session tokens
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.split(" ")[1]

    # 1. Check admin session first
    if verify_admin_session_token(token):
        return ADMIN_USER_ID

    # 2. Fall back to Firebase
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# Keep the old name so existing imports don't break
verify_firebase_token = verify_token
