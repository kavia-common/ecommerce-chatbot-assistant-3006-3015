"""
Chat router: endpoints for chat interactions and Q&A.
Ocean Professional notes for frontend:
- Display assistant responses in a clean chat bubble with blue accent for user and neutral for assistant.
- Use subtle shadows and rounded corners.
"""
from fastapi import APIRouter, HTTPException
from ..models import ChatRequest, ChatResponse, QARequest, QAResponse
from ..services import generate_chat_reply, answer_question
from ..store import SESSION_STORE

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "",
    summary="Send chat messages",
    operation_id="chat_send",
    response_model=ChatResponse,
    responses={400: {"description": "Invalid request"}},
)
def chat_send(payload: ChatRequest):
    """
    Chat endpoint to send a series of messages and receive the assistant reply.

    Request body:
        - session_id: optional string for continuing an existing session
        - messages: ordered list of messages, last one should be the user's latest input
        - context: optional key-value context (e.g., cart items, user profile)

    Returns:
        ChatResponse: containing session_id, reply text, and metadata.

    Notes:
        - If session_id is not provided, a new session is created automatically.
        - Messages are appended to the session store for continuity.
    """
    if not payload.messages:
        raise HTTPException(status_code=400, detail="messages list cannot be empty")

    session_id = payload.session_id or SESSION_STORE.create(initial_context=payload.context or {})
    if payload.session_id and payload.context:
        SESSION_STORE.update_context(session_id, payload.context)

    # Persist incoming messages
    for m in payload.messages:
        SESSION_STORE.append_message(session_id, m.role, m.content)

    result = generate_chat_reply(payload.messages, payload.context)
    SESSION_STORE.append_message(session_id, "assistant", result["reply"])
    return ChatResponse(session_id=session_id, reply=result["reply"], metadata=result.get("metadata", {}))


# PUBLIC_INTERFACE
@router.post(
    "/qa",
    summary="Answer a user question",
    operation_id="chat_qa",
    response_model=QAResponse,
)
def chat_qa(payload: QARequest):
    """
    Q&A endpoint for product or policy questions.

    Request body:
        - question: the text question
        - product_ids: optional list to scope the answer to specific products

    Returns:
        QAResponse with the answer, related product IDs, and a confidence score.

    Tips (frontend):
        - Use amber accents (#F59E0B) to highlight key facts in the answer.
        - If confidence < 0.75, consider showing a subtle disclaimer banner.
    """
    result = answer_question(payload.question, payload.product_ids)
    return QAResponse(**result)
