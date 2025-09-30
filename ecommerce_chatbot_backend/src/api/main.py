"""
Ocean Professional Backend - Ecommerce Chatbot API
Color accents: primary #2563EB, secondary #F59E0B, error #EF4444, background #f9fafb

This module defines the FastAPI application, sets up CORS, routing, and OpenAPI metadata.
The API is designed with a modern, modular structure for maintainability and future
integration with real ecommerce platforms and LLM providers.

Environment:
- Load configuration from environment variables using python-dotenv if present.
- Do not commit real secrets. Ask orchestrator to set env values in .env at deploy.

Style hints for frontend (Ocean Professional):
- Use blue (#2563EB) for primary CTAs and highlights.
- Amber (#F59E0B) as accent for success or recommend badges.
- Respect minimal layout with spacing and subtle shadows for cards.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat, recommendations, products, health, sessions
from .config import get_settings
from .openapi_meta import app_tags, app_contact, app_license

settings = get_settings()

# Initialize FastAPI with metadata and tags for OpenAPI/Swagger
app = FastAPI(
    title="Ecommerce Chatbot API",
    description=(
        "A modern, modular FastAPI backend powering an ecommerce chatbot.\n\n"
        "Features:\n"
        "- Natural language chat interface\n"
        "- Product Q&A\n"
        "- Personalized recommendations\n"
        "- Product search proxy\n\n"
        "Ocean Professional theme: blue primary, amber accents; clean and minimal."
    ),
    version="1.0.0",
    contact=app_contact,
    license_info=app_license,
    openapi_tags=app_tags,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with prefixes and tags
app.include_router(health.router, prefix="", tags=["Health"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])


# PUBLIC_INTERFACE
@app.get("/docs/websocket-usage", tags=["Docs"], summary="WebSocket usage (future)")
def websocket_usage_note():
    """
    WebSocket usage documentation note.

    This backend is currently REST-first. If a WebSocket endpoint is introduced for
    real-time chat streaming, it will be documented here with connection details and
    authentication notes, including:
    - ws(s)://<host>/ws/chat
    - Headers: Authorization: Bearer <token> (if enabled)
    - Message format: JSON frames with role/content tokens

    Returns:
        dict: A placeholder description and status for WebSocket plans.
    """
    return {
        "status": "planned",
        "message": "WebSocket streaming is planned for a future version. Currently REST endpoints are available for chat, Q&A, and recommendations."
    }
