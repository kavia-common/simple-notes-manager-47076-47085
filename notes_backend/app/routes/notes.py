from datetime import datetime
from typing import Dict, Any, List

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request

# In-memory storage for notes
# Simple incrementing integer ID
_NOTES: Dict[int, Dict[str, Any]] = {}
_NEXT_ID: int = 1

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="CRUD operations for text notes",
)


def _now_iso() -> str:
    """Return current UTC time in ISO 8601 format."""
    return datetime.utcnow().isoformat() + "Z"


def _validate_note_payload(payload: Dict[str, Any], require_title: bool = True) -> Dict[str, Any]:
    """
    Validate incoming JSON payload for note creation/update.

    - title (required by default, non-empty string)
    - content (optional, string)
    """
    if not isinstance(payload, dict):
        abort(400, message="Invalid JSON body")

    title = payload.get("title")
    content = payload.get("content")

    if require_title:
        if title is None or not isinstance(title, str) or not title.strip():
            abort(400, message="Field 'title' is required and must be a non-empty string.")
    else:
        if title is not None and (not isinstance(title, str) or not title.strip()):
            abort(400, message="If provided, 'title' must be a non-empty string.")

    if content is not None and not isinstance(content, str):
        abort(400, message="If provided, 'content' must be a string.")

    return {
        "title": title.strip() if isinstance(title, str) else None,
        "content": content if isinstance(content, str) else None,
    }


def _get_note_or_404(note_id: int) -> Dict[str, Any]:
    """Fetch a note by ID or abort with 404."""
    note = _NOTES.get(note_id)
    if note is None:
        abort(404, message="Note not found")
    return note


@blp.route("/")
class NotesCollection(MethodView):
    """
    Methods for interacting with the collection of notes.
    """

    # PUBLIC_INTERFACE
    def get(self):
        """List all notes."""
        notes: List[Dict[str, Any]] = list(_NOTES.values())
        return notes, 200

    # PUBLIC_INTERFACE
    def post(self):
        """Create a new note with title (required) and content (optional)."""
        if not request.is_json:
            abort(400, message="Expected application/json")
        data = request.get_json() or {}
        validated = _validate_note_payload(data, require_title=True)

        global _NEXT_ID
        note_id = _NEXT_ID
        _NEXT_ID += 1

        now = _now_iso()
        note = {
            "id": note_id,
            "title": validated["title"],
            "content": validated["content"] or "",
            "created_at": now,
            "updated_at": now,
        }
        _NOTES[note_id] = note
        return note, 201


@blp.route("/<int:note_id>")
class NoteResource(MethodView):
    """
    Methods for interacting with a single note by id.
    """

    # PUBLIC_INTERFACE
    def get(self, note_id: int):
        """Retrieve a note by id."""
        note = _get_note_or_404(note_id)
        return note, 200

    # PUBLIC_INTERFACE
    def put(self, note_id: int):
        """Update a note title/content (either field may be provided)."""
        if not request.is_json:
            abort(400, message="Expected application/json")
        data = request.get_json() or {}
        validated = _validate_note_payload(data, require_title=False)

        note = _get_note_or_404(note_id)

        changed = False
        if validated["title"] is not None:
            note["title"] = validated["title"]
            changed = True
        if validated["content"] is not None:
            note["content"] = validated["content"]
            changed = True

        if changed:
            note["updated_at"] = _now_iso()

        return note, 200

    # PUBLIC_INTERFACE
    def delete(self, note_id: int):
        """Delete a note by id."""
        _get_note_or_404(note_id)
        del _NOTES[note_id]
        # Return a 204 No Content to meet acceptance criteria option
        return "", 204
