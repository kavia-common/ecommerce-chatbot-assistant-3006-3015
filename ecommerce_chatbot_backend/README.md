# Ecommerce Chatbot Backend (FastAPI)

Modern, modular FastAPI backend for an ecommerce chatbot.
Ocean Professional theme: blue primary (#2563EB), amber accents (#F59E0B), minimalist and clean.

## Features
- Chat endpoint for natural language interactions
- Q&A endpoint for product/policy questions
- Product search and product detail endpoints (mock provider)
- Recommendation endpoint (built-in heuristic)
- Session management endpoints
- OpenAPI docs with clear tags and summaries

## Quickstart

1) Install dependencies
```
pip install -r requirements.txt
# Note: If your environment was provisioned before this fix and lacks pydantic-settings,
# install it explicitly:
# pip install pydantic-settings==2.6.1
```

2) Run locally
```
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

3) Open API Docs
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

## Environment

Set the following variables via a .env file (do not commit secrets):

Example `.env.example`:
```
APP_NAME=Ecommerce Chatbot API
ENV=development
DEBUG=true
LOG_LEVEL=INFO
CORS_ALLOW_ORIGINS=["*"]

LLM_PROVIDER=mock
LLM_MODEL=mock-chat-001
OPENAI_API_KEY=

PRODUCT_PROVIDER=mock
PRODUCT_SOURCE_URL=

RECOMMENDER_PROVIDER=builtin
MAX_RECOMMENDATIONS=6
```

Note: Ask the orchestrator to set environment variables in the deployment environment.

## Endpoints Overview

- GET `/` (Health) — health check
- POST `/chat` — send messages and get assistant reply
- POST `/chat/qa` — ask a question and get an answer
- POST `/products/search` — search products
- GET `/products/{product_id}` — get product details
- POST `/recommendations` — get recommended products
- POST `/sessions` — create a session
- GET `/sessions` — list sessions
- GET `/sessions/{session_id}` — get a session
- DELETE `/sessions/{session_id}` — delete a session
- GET `/docs/websocket-usage` — note for future WebSocket support

## Architecture

- api/main.py — app creation, metadata, router mounting
- api/config.py — Pydantic settings loaded from env
- api/openapi_meta.py — OpenAPI tags, contact, license
- api/models.py — request/response models
- api/services.py — business logic (mock implementations)
- api/store.py — in-memory session store and product catalog
- api/routers/ — endpoint modules by domain

## Ocean Professional Frontend Hints

- Primary accents: #2563EB (buttons, focus states)
- Secondary accents: #F59E0B (badges, highlights)
- Error: #EF4444
- Surfaces: #ffffff on #f9fafb background
- Use subtle shadows and rounded corners for cards
- Keep spacing generous; minimal borders; prefer elevation to separate content

## Integration Notes

- Replace mock services with real providers:
  - LLM: switch LLM_PROVIDER and supply API keys
  - Products: implement real product provider in services and store
  - Recommender: attach to analytics/events or a vector store
- Add authentication (API keys/JWT) before production
- Replace in-memory session store with Redis/Postgres for scale

## License
MIT
