"""
Supabase client — replaces Firebase Admin SDK for database operations.

This module provides a `db`-like interface using Supabase,
keeping the same import pattern: `from app.utils.firebase import db`
"""
import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")


def _init_supabase() -> Client:
    """Initialize the Supabase client with the service role key."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set "
            "for Supabase database operations."
        )
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


# Lazy-init singleton
_client: Client = None


def get_client() -> Client:
    """Get the Supabase client singleton."""
    global _client
    if _client is None:
        _client = _init_supabase()
    return _client


class SupabaseCollection:
    """
    Thin wrapper that mimics the Firestore collection/document API
    used throughout the storage_service. Routes reads/writes to
    Supabase REST via the supabase-py client.

    Collection naming convention maps to Supabase tables:
      - users/<id>                    → table: users,         row: id = <id>
      - users/<id>/active_roadmap/current → table: roadmaps,   row: user_id = <id>
      - users/<id>/analyses           → table: analyses,      row: user_id = <id>
    """

    def __init__(self, name: str):
        self.name = name

    def document(self, doc_id: str):
        return SupabaseDocument(self.name, doc_id)

    def add(self, data: dict):
        """Add a document with auto-generated ID."""
        client = get_client()
        # For analyses collection, insert with user_id
        table = self.name.split("/")[-1] if "/" in self.name else self.name
        client.table(table).insert(data).execute()


class SupabaseDocument:
    def __init__(self, collection_path: str, doc_id: str):
        self.collection_path = collection_path
        self.doc_id = doc_id

    @property
    def _table_name(self):
        """Determine Supabase table from collection path."""
        parts = self.collection_path.split("/")
        if "active_roadmap" in self.collection_path:
            return "roadmaps"
        elif "analyses" in self.collection_path:
            return "analyses"
        else:
            return "users"

    @property
    def _row_filter(self):
        """Determine the row filter for this document."""
        parts = self.collection_path.split("/")
        if "active_roadmap" in self.collection_path:
            # Extract user_id from path like users/<id>/active_roadmap
            user_id = parts[1] if len(parts) > 1 else self.doc_id
            return {"user_id": user_id}
        elif "analyses" in self.collection_path:
            user_id = parts[1] if len(parts) > 1 else self.doc_id
            return {"user_id": user_id}
        else:
            return {"id": self.doc_id}

    def get(self):
        """Get a single document."""
        client = get_client()
        table = self._table_name
        filter_dict = self._row_filter

        result = client.table(table).select("*").filter(
            list(filter_dict.keys())[0],
            "eq",
            list(filter_dict.values())[0]
        ).execute()

        if result.data and len(result.data) > 0:
            return SupabaseDocSnapshot(result.data[0], exists=True)
        return SupabaseDocSnapshot(None, exists=False)

    def set(self, data: dict, merge: bool = False):
        """Set a document."""
        client = get_client()
        table = self._table_name
        filter_dict = self._row_filter

        if merge:
            # Check if exists first
            existing = client.table(table).select("*").filter(
                list(filter_dict.keys())[0],
                "eq",
                list(filter_dict.values())[0]
            ).execute()

            if existing.data and len(existing.data) > 0:
                # Update
                client.table(table).update(data).filter(
                    list(filter_dict.keys())[0],
                    "eq",
                    list(filter_dict.values())[0]
                ).execute()
            else:
                # Insert
                data[list(filter_dict.keys())[0]] = list(filter_dict.values())[0]
                client.table(table).insert(data).execute()
        else:
            # Delete existing and insert
            client.table(table).delete().filter(
                list(filter_dict.keys())[0],
                "eq",
                list(filter_dict.values())[0]
            ).execute()
            data[list(filter_dict.keys())[0]] = list(filter_dict.values())[0]
            client.table(table).insert(data).execute()

    def update(self, data: dict):
        """Update a document."""
        client = get_client()
        table = self._table_name
        filter_dict = self._row_filter

        client.table(table).update(data).filter(
            list(filter_dict.keys())[0],
            "eq",
            list(filter_dict.values())[0]
        ).execute()

    def delete(self):
        """Delete a document."""
        client = get_client()
        table = self._table_name
        filter_dict = self._row_filter

        client.table(table).delete().filter(
            list(filter_dict.keys())[0],
            "eq",
            list(filter_dict.values())[0]
        ).execute()


class SupabaseDocSnapshot:
    """Mimics a Firestore DocumentSnapshot."""
    def __init__(self, data: dict = None, exists: bool = False):
        self._data = data
        self.exists = exists

    def to_dict(self):
        return self._data


def collection(path: str) -> SupabaseCollection:
    """Access a collection by path (e.g., 'users')."""
    return SupabaseCollection(path)


# Backward-compatible `db` object
class _SupabaseDB:
    """Drop-in replacement for `firestore.client()` with collection() method."""
    def collection(self, name: str) -> SupabaseCollection:
        return SupabaseCollection(name)

    def _test_connection(self):
        """Quick connectivity test."""
        client = get_client()
        client.table("users").select("id").limit(1).execute()


db = _SupabaseDB()
