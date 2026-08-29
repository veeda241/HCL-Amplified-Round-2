from datetime import datetime
import traceback
import threading
import os

from app.services import local_storage as _local

# Determine Firebase availability
# If FIREBASE_PROJECT_ID env var is not set, skip Firebase entirely
_firebase_available = None  # None = untested, True = working, False = broken

def _init_firebase():
    """Lazily initialize and test Firebase. Returns True if working."""
    global _firebase_available

    # If no Firebase env vars, don't even try
    if not os.getenv("FIREBASE_PROJECT_ID"):
        print("INFO: No FIREBASE_PROJECT_ID set — using local file storage")
        _firebase_available = False
        return False

    try:
        from app.utils.firebase import db
    except Exception as e:
        print(f"WARNING: Firebase import failed ({e}), using local file storage")
        _firebase_available = False
        return False

    # Test connectivity with timeout
    result = [False]

    def _check():
        try:
            db.collection("__health_check__").limit(1).get()
            result[0] = True
        except Exception:
            result[0] = False

    t = threading.Thread(target=_check, daemon=True)
    t.start()
    t.join(timeout=5)
    if t.is_alive():
        print("WARNING: Firebase health check timed out, using local file storage")
        _firebase_available = False
        return False

    if not result[0]:
        print("WARNING: Firebase health check failed, using local file storage")
        _firebase_available = False
        return False

    _firebase_available = True
    return True


def _use_firebase():
    global _firebase_available
    if _firebase_available is None:
        return _init_firebase()
    return _firebase_available


def _firebase_failed():
    global _firebase_available
    _firebase_available = False
    print("WARNING: Firebase disabled for this session, using local file storage")


def _get_db():
    from app.utils.firebase import db
    return db


def save_career_analysis(user_id: str, profile: dict, career_decision: dict, roadmap: dict):
    if _use_firebase():
        try:
            db = _get_db()
            data = {
                "profile": profile,
                "career_decision": career_decision,
                "roadmap": roadmap,
                "created_at": datetime.utcnow()
            }
            db.collection("users").document(user_id).collection("analyses").add(data)
            save_active_roadmap(user_id, career_decision, roadmap)
            return True
        except Exception as e:
            print(f"WARNING: Firebase save failed ({e}), switching to local storage")
            _firebase_failed()
    return _local.save_career_analysis(user_id, profile, career_decision, roadmap)


def save_active_roadmap(user_id: str, career_decision: dict, roadmap: dict, preserve_progress: bool = False):
    if _use_firebase():
        try:
            db = _get_db()
            existing_data = None
            if preserve_progress:
                existing_data = get_active_roadmap(user_id)

            if "roadmap" in roadmap:
                for idx, phase in enumerate(roadmap["roadmap"]):
                    if existing_data and preserve_progress:
                        old_roadmap = existing_data.get("learning_roadmap", {}).get("roadmap", [])
                        if idx < len(old_roadmap):
                            old_phase = old_roadmap[idx]
                            if old_phase.get("status") == "completed":
                                phase["status"] = "completed"
                                phase["completed_at"] = old_phase.get("completed_at")
                            else:
                                phase["status"] = "pending"
                                phase["completed_at"] = None
                        else:
                            phase["status"] = "pending"
                            phase["completed_at"] = None
                    else:
                        phase["status"] = "pending"
                        phase["completed_at"] = None

            if existing_data and preserve_progress:
                completed_count = sum(1 for p in roadmap.get("roadmap", []) if p.get("status") == "completed")
                progress_data = {
                    "completed_phases": completed_count,
                    "total_phases": len(roadmap.get("roadmap", [])),
                    "streak_days": existing_data.get("progress", {}).get("streak_days", 0),
                    "last_activity_date": existing_data.get("progress", {}).get("last_activity_date")
                }
            else:
                progress_data = {
                    "completed_phases": 0,
                    "total_phases": len(roadmap.get("roadmap", [])),
                    "streak_days": 0,
                    "last_activity_date": None
                }

            data = {
                "career_decision": career_decision,
                "learning_roadmap": roadmap,
                "progress": progress_data,
                "updated_at": datetime.utcnow()
            }
            db.collection("users").document(user_id).collection("active_roadmap").document("current").set(data)
            return True
        except Exception as e:
            print(f"WARNING: Firebase save failed ({e}), switching to local storage")
            _firebase_failed()
    return _local.save_active_roadmap(user_id, career_decision, roadmap, preserve_progress)


def get_active_roadmap(user_id: str):
    if _use_firebase():
        try:
            db = _get_db()
            doc = db.collection("users").document(user_id).collection("active_roadmap").document("current").get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            print(f"WARNING: Firebase read failed ({e}), switching to local storage")
            _firebase_failed()
    return _local.get_active_roadmap(user_id)


def update_phase_status(user_id: str, phase_index: int, status: str):
    if _use_firebase():
        try:
            db = _get_db()
            ref = db.collection("users").document(user_id).collection("active_roadmap").document("current")
            doc = ref.get()
            if not doc.exists:
                return False

            data = doc.to_dict()
            roadmap = data.get("learning_roadmap", {}).get("roadmap", [])

            if 0 <= phase_index < len(roadmap):
                roadmap[phase_index]["status"] = status
                if status == "completed":
                    roadmap[phase_index]["completed_at"] = datetime.utcnow().isoformat()
                    completed_count = sum(1 for p in roadmap if p.get("status") == "completed")
                    data["progress"]["completed_phases"] = completed_count
                    update_streak(data["progress"])

                ref.update({
                    "learning_roadmap.roadmap": roadmap,
                    "progress": data["progress"],
                    "updated_at": datetime.utcnow()
                })
                return True
            return False
        except Exception as e:
            print(f"WARNING: Firebase update failed ({e}), switching to local storage")
            _firebase_failed()
    return _local.update_phase_status(user_id, phase_index, status)


def update_streak(progress_data: dict):
    now = datetime.utcnow()
    last_active = progress_data.get("last_activity_date")

    if last_active:
        last_date = datetime.fromisoformat(last_active).date()
        today = now.date()
        diff = (today - last_date).days

        if diff == 1:
            progress_data["streak_days"] += 1
        elif diff > 1:
            progress_data["streak_days"] = 1
    else:
        progress_data["streak_days"] = 1

    progress_data["last_activity_date"] = now.isoformat()


def get_student_profile(user_id: str):
    if _use_firebase():
        try:
            db = _get_db()
            doc = db.collection("users").document(user_id).get()
            if doc.exists:
                data = doc.to_dict()
                return data.get("profile")
        except Exception as e:
            print(f"WARNING: Firebase read failed ({e}), switching to local storage")
            _firebase_failed()
    return _local.get_student_profile(user_id)


def save_student_profile(user_id: str, profile: dict):
    if _use_firebase():
        try:
            db = _get_db()
            print(f"Saving to Firestore for user: {user_id}")
            db.collection("users").document(user_id).set({
                "profile": profile,
                "updated_at": datetime.utcnow()
            }, merge=True)
            print(f"Successfully saved to Firestore for user: {user_id}")
            return True
        except Exception as e:
            print(f"WARNING: Firebase save failed ({e}), switching to local storage")
            traceback.print_exc()
            _firebase_failed()
    return _local.save_student_profile(user_id, profile)


def delete_active_roadmap(user_id: str):
    if _use_firebase():
        try:
            db = _get_db()
            ref = db.collection("users").document(user_id).collection("active_roadmap").document("current")
            doc = ref.get()
            if doc.exists:
                ref.delete()
                return True
            return False
        except Exception as e:
            print(f"WARNING: Firebase delete failed ({e}), switching to local storage")
            _firebase_failed()
    return _local.delete_active_roadmap(user_id)
