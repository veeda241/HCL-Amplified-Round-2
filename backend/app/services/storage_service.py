from datetime import datetime
import traceback
import os

from app.services import local_storage as _local

# Determine Supabase availability
_supabase_available = None  # None = untested, True = working, False = broken


def _init_supabase():
    """Lazily initialize and test Supabase. Returns True if working."""
    global _supabase_available

    # If no Supabase env vars, don't even try
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_SERVICE_KEY"):
        print("INFO: No SUPABASE_URL/SUPABASE_SERVICE_KEY set — using local file storage")
        _supabase_available = False
        return False

    try:
        from app.utils.firebase import db, get_client
        client = get_client()
        # Quick connectivity test
        client.table("users").select("id").limit(1).execute()
        print("INFO: Supabase connection successful")
        _supabase_available = True
        return True
    except Exception as e:
        print(f"WARNING: Supabase connection failed ({e}), using local file storage")
        _supabase_available = False
        return False


def _use_supabase():
    global _supabase_available
    if _supabase_available is None:
        return _init_supabase()
    return _supabase_available


def _supabase_failed():
    global _supabase_available
    _supabase_available = False
    print("WARNING: Supabase disabled for this session, using local file storage")


def _get_client():
    from app.utils.firebase import get_client
    return get_client()


# ── Career Analysis ──────────────────────────────────────────────

def save_career_analysis(user_id: str, profile: dict, career_decision: dict, roadmap: dict):
    if _use_supabase():
        try:
            client = _get_client()
            data = {
                "user_id": user_id,
                "profile": profile,
                "career_decision": career_decision,
                "roadmap": roadmap,
                "created_at": datetime.utcnow().isoformat()
            }
            client.table("analyses").insert(data).execute()
            save_active_roadmap(user_id, career_decision, roadmap)
            return True
        except Exception as e:
            print(f"WARNING: Supabase save failed ({e}), switching to local storage")
            _supabase_failed()
    return _local.save_career_analysis(user_id, profile, career_decision, roadmap)


# ── Active Roadmap ───────────────────────────────────────────────

def save_active_roadmap(user_id: str, career_decision: dict, roadmap: dict, preserve_progress: bool = False):
    if _use_supabase():
        try:
            client = _get_client()
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

            # Upsert: check if exists
            existing = client.table("roadmaps").select("id").eq("user_id", user_id).execute()
            if existing.data:
                client.table("roadmaps").update(data).eq("user_id", user_id).execute()
            else:
                data["user_id"] = user_id
                client.table("roadmaps").insert(data).execute()
            return True
        except Exception as e:
            print(f"WARNING: Supabase save failed ({e}), switching to local storage")
            _supabase_failed()
    return _local.save_active_roadmap(user_id, career_decision, roadmap, preserve_progress)


def get_active_roadmap(user_id: str):
    if _use_supabase():
        try:
            client = _get_client()
            result = client.table("roadmaps").select("*").eq("user_id", user_id).execute()
            if result.data and len(result.data) > 0:
                return result.data[0]
            return None
        except Exception as e:
            print(f"WARNING: Supabase read failed ({e}), switching to local storage")
            _supabase_failed()
    return _local.get_active_roadmap(user_id)


def update_phase_status(user_id: str, phase_index: int, status: str):
    if _use_supabase():
        try:
            client = _get_client()
            result = client.table("roadmaps").select("*").eq("user_id", user_id).execute()
            if not result.data:
                return False

            data = result.data[0]
            roadmap = data.get("learning_roadmap", {}).get("roadmap", [])

            if 0 <= phase_index < len(roadmap):
                roadmap[phase_index]["status"] = status
                if status == "completed":
                    roadmap[phase_index]["completed_at"] = datetime.utcnow().isoformat()
                    completed_count = sum(1 for p in roadmap if p.get("status") == "completed")
                    data["progress"]["completed_phases"] = completed_count
                    update_streak(data["progress"])

                client.table("roadmaps").update({
                    "learning_roadmap": data["learning_roadmap"],
                    "progress": data["progress"],
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("user_id", user_id).execute()
                return True
            return False
        except Exception as e:
            print(f"WARNING: Supabase update failed ({e}), switching to local storage")
            _supabase_failed()
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


# ── Student Profile ──────────────────────────────────────────────

def get_student_profile(user_id: str):
    if _use_supabase():
        try:
            client = _get_client()
            result = client.table("users").select("profile").eq("id", user_id).execute()
            if result.data and len(result.data) > 0:
                return result.data[0].get("profile")
            return None
        except Exception as e:
            print(f"WARNING: Supabase read failed ({e}), switching to local storage")
            _supabase_failed()
    return _local.get_student_profile(user_id)


def save_student_profile(user_id: str, profile: dict):
    if _use_supabase():
        try:
            client = _get_client()
            print(f"Saving to Supabase for user: {user_id}")

            # Upsert
            existing = client.table("users").select("id").eq("id", user_id).execute()
            if existing.data:
                client.table("users").update({
                    "profile": profile,
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("id", user_id).execute()
            else:
                client.table("users").insert({
                    "id": user_id,
                    "profile": profile,
                    "updated_at": datetime.utcnow().isoformat()
                }).execute()

            print(f"Successfully saved to Supabase for user: {user_id}")
            return True
        except Exception as e:
            print(f"WARNING: Supabase save failed ({e}), switching to local storage")
            traceback.print_exc()
            _supabase_failed()
    return _local.save_student_profile(user_id, profile)


def delete_active_roadmap(user_id: str):
    if _use_supabase():
        try:
            client = _get_client()
            existing = client.table("roadmaps").select("id").eq("user_id", user_id).execute()
            if existing.data:
                client.table("roadmaps").delete().eq("user_id", user_id).execute()
                return True
            return False
        except Exception as e:
            print(f"WARNING: Supabase delete failed ({e}), switching to local storage")
            _supabase_failed()
    return _local.delete_active_roadmap(user_id)
