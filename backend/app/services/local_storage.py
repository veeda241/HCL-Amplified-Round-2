"""
Local file-based storage fallback.
Used when Firebase is unavailable. Stores data in JSON files under backend/local_data/.
"""
import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "local_data")


def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _user_dir(user_id: str) -> str:
    d = os.path.join(DATA_DIR, user_id)
    os.makedirs(d, exist_ok=True)
    return d


def save_career_analysis(user_id: str, profile: dict, career_decision: dict, roadmap: dict):
    """Save career analysis to local JSON file."""
    _ensure_dir()
    data = {
        "profile": profile,
        "career_decision": career_decision,
        "roadmap": roadmap,
        "created_at": datetime.utcnow().isoformat()
    }
    path = os.path.join(_user_dir(user_id), "analysis.json")
    with open(path, "w") as f:
        json.dump(data, f, default=str, indent=2)

    save_active_roadmap(user_id, career_decision, roadmap)
    return True


def save_active_roadmap(user_id: str, career_decision: dict, roadmap: dict, preserve_progress: bool = False):
    """Save active roadmap to local JSON file."""
    _ensure_dir()
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
        "updated_at": datetime.utcnow().isoformat()
    }

    path = os.path.join(_user_dir(user_id), "active_roadmap.json")
    with open(path, "w") as f:
        json.dump(data, f, default=str, indent=2)
    return True


def get_active_roadmap(user_id: str):
    """Get active roadmap from local JSON file."""
    _ensure_dir()
    path = os.path.join(_user_dir(user_id), "active_roadmap.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def update_phase_status(user_id: str, phase_index: int, status: str):
    """Update a phase's status in the local roadmap."""
    data = get_active_roadmap(user_id)
    if not data:
        return False

    roadmap = data.get("learning_roadmap", {}).get("roadmap", [])
    if 0 <= phase_index < len(roadmap):
        roadmap[phase_index]["status"] = status
        if status == "completed":
            roadmap[phase_index]["completed_at"] = datetime.utcnow().isoformat()
            completed_count = sum(1 for p in roadmap if p.get("status") == "completed")
            data["progress"]["completed_phases"] = completed_count
            # Update streak
            now = datetime.utcnow()
            last_active = data["progress"].get("last_activity_date")
            if last_active:
                last_date = datetime.fromisoformat(last_active).date()
                diff = (now.date() - last_date).days
                if diff == 1:
                    data["progress"]["streak_days"] += 1
                elif diff > 1:
                    data["progress"]["streak_days"] = 1
            else:
                data["progress"]["streak_days"] = 1
            data["progress"]["last_activity_date"] = now.isoformat()

        path = os.path.join(_user_dir(user_id), "active_roadmap.json")
        with open(path, "w") as f:
            json.dump(data, f, default=str, indent=2)
        return True
    return False


def delete_active_roadmap(user_id: str):
    """Delete active roadmap from local storage."""
    _ensure_dir()
    path = os.path.join(_user_dir(user_id), "active_roadmap.json")
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def save_student_profile(user_id: str, profile: dict):
    """Save student profile to local JSON file."""
    _ensure_dir()
    path = os.path.join(_user_dir(user_id), "profile.json")
    data = {
        "profile": profile,
        "updated_at": datetime.utcnow().isoformat()
    }
    with open(path, "w") as f:
        json.dump(data, f, default=str, indent=2)
    return True


def get_student_profile(user_id: str):
    """Get student profile from local JSON file."""
    _ensure_dir()
    path = os.path.join(_user_dir(user_id), "profile.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        data = json.load(f)
    return data.get("profile")
