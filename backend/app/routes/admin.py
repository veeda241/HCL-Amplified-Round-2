from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from app.utils.auth import create_admin_session, verify_admin_session_token
import os

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)


class AdminLoginRequest(BaseModel):
    email: str
    password: str


class AdminLoginResponse(BaseModel):
    success: bool
    message: str
    admin_email: str
    token: str


@router.post("/login")
def admin_login(request: AdminLoginRequest):
    """Admin login with email/password (no Firebase needed)"""
    admin_email = os.getenv("ADMIN_EMAIL", "admin@skillroute.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    if request.email == admin_email and request.password == admin_password:
        token = create_admin_session(admin_email)
        return AdminLoginResponse(
            success=True,
            message="Admin login successful",
            admin_email=admin_email,
            token=token
        )
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials"
        )


@router.get("/verify")
def verify_admin(authorization: str = Header(...)):
    """Verify admin session (no Firebase needed)"""
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else ""
    if not verify_admin_session_token(token):
        raise HTTPException(status_code=401, detail="Invalid admin session")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@skillroute.com")
    return {"is_admin": True, "email": admin_email}


@router.get("/users")
def get_all_users(authorization: str = Header(...)):
    """Get all users (admin only)"""
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else ""
    if not verify_admin_session_token(token):
        raise HTTPException(status_code=401, detail="Invalid admin session")

    try:
        # Lazy import to avoid Firebase init at startup
        from app.services.storage_service import _use_firebase
        if _use_firebase():
            from app.utils.firebase import db
            users_ref = db.collection('students')
            docs = users_ref.stream()
            users = []
            for doc in docs:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                users.append(user_data)
            return {"users": users, "total": len(users)}
        else:
            # Local storage fallback
            from app.services import local_storage as _local

            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "local_data")
            users = []
            if os.path.exists(data_dir):
                for user_id in os.listdir(data_dir):
                    user_dir = os.path.join(data_dir, user_id)
                    if os.path.isdir(user_dir):
                        profile = _local.get_student_profile(user_id)
                        if profile:
                            users.append({"id": user_id, **profile})
            return {"users": users, "total": len(users)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_admin_stats(authorization: str = Header(...)):
    """Get platform statistics (admin only)"""
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else ""
    if not verify_admin_session_token(token):
        raise HTTPException(status_code=401, detail="Invalid admin session")

    try:
        from app.services.storage_service import _use_firebase
        if _use_firebase():
            from app.utils.firebase import db
            users_count = len(list(db.collection('students').stream()))
            roadmaps_count = len(list(db.collection('roadmaps').stream()))
            quizzes_count = len(list(db.collection('quizzes').stream()))
        else:
            # Local storage stats
            import os
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "local_data")
            users_count = 0
            roadmaps_count = 0
            quizzes_count = 0
            if os.path.exists(data_dir):
                for user_id in os.listdir(data_dir):
                    user_dir = os.path.join(data_dir, user_id)
                    if os.path.isdir(user_dir):
                        users_count += 1
                        if os.path.exists(os.path.join(user_dir, "active_roadmap.json")):
                            roadmaps_count += 1

        return {
            "total_users": users_count,
            "total_roadmaps": roadmaps_count,
            "total_quizzes": quizzes_count,
            "status": "active"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
