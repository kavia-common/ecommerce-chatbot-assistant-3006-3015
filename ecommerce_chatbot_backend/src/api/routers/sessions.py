"""
Sessions router: create, view, update, delete chat sessions.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from ..models import CreateSessionRequest, SessionInfo
from ..store import SESSION_STORE

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "",
    summary="Create a chat session",
    operation_id="sessions_create",
    response_model=SessionInfo,
)
def create_session(payload: CreateSessionRequest):
    """
    Create a new chat session.

    Request body:
        - initial_context: optional dict to seed session context

    Returns:
        SessionInfo including session_id and created_at ISO string.
    """
    sid = SESSION_STORE.create(initial_context=payload.initial_context or {})
    data = SESSION_STORE.get(sid)
    return SessionInfo(session_id=sid, created_at=data["created_at"], context=data["context"])


# PUBLIC_INTERFACE
@router.get(
    "",
    summary="List sessions",
    operation_id="sessions_list",
    response_model=List[SessionInfo],
)
def list_sessions():
    """
    List all active sessions (in-memory mock).

    Returns:
        List[SessionInfo]
    """
    all_sessions = SESSION_STORE.list()
    return [SessionInfo(session_id=s["session_id"], created_at=s["created_at"], context=s["context"]) for s in all_sessions]


# PUBLIC_INTERFACE
@router.get(
    "/{session_id}",
    summary="Get a session",
    operation_id="sessions_get",
    response_model=SessionInfo,
    responses={404: {"description": "Session not found"}},
)
def get_session(session_id: str):
    """
    Get session details by ID.

    Path params:
        - session_id: string

    Returns:
        SessionInfo

    Raises:
        404 if not found
    """
    data = SESSION_STORE.get(session_id)
    if not data:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionInfo(session_id=session_id, created_at=data["created_at"], context=data["context"])


# PUBLIC_INTERFACE
@router.delete(
    "/{session_id}",
    summary="Delete a session",
    operation_id="sessions_delete",
    responses={204: {"description": "Deleted"}, 404: {"description": "Session not found"}},
)
def delete_session(session_id: str):
    """
    Delete a session by ID.

    Returns:
        204 No Content on success, 404 otherwise.
    """
    ok = SESSION_STORE.delete(session_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}
