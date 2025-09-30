"""
In-memory stores and utilities.

Note:
- For production, replace with a database or cache (Redis/Postgres).
- This module provides a simple session store and a mock product catalog.

Ocean Professional: Simple, readable, with graceful fallbacks.
"""
from __future__ import annotations
import time
import uuid
from typing import Dict, Any, List, Optional
from .models import Product


class SessionStore:
    """A naive in-memory session store suitable for demos and local dev."""
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def create(self, initial_context: Optional[dict] = None) -> str:
        sid = str(uuid.uuid4())
        self._sessions[sid] = {
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "context": initial_context or {},
            "messages": [],
        }
        return sid

    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._sessions.get(session_id)

    def update_context(self, session_id: str, patch: dict) -> Optional[Dict[str, Any]]:
        sess = self._sessions.get(session_id)
        if not sess:
            return None
        sess["context"].update(patch or {})
        return sess

    def append_message(self, session_id: str, role: str, content: str) -> None:
        sess = self._sessions.get(session_id)
        if not sess:
            return
        sess["messages"].append({"role": role, "content": content})

    def list(self) -> List[Dict[str, Any]]:
        return [{"session_id": sid, **data} for sid, data in self._sessions.items()]

    def delete(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None


SESSION_STORE = SessionStore()


MOCK_PRODUCTS: List[Product] = [
    Product(id="sku-1001", title="Ocean Breeze Hoodie", description="Soft cotton hoodie with ocean blue tone.", price=49.99, currency="USD", image_url="https://picsum.photos/id/21/300/200"),
    Product(id="sku-1002", title="Amber Trail Sneakers", description="Lightweight sneakers with amber accents.", price=89.0, currency="USD", image_url="https://picsum.photos/id/22/300/200"),
    Product(id="sku-1003", title="Skyline Laptop Sleeve", description="Neoprene sleeve with minimalist design.", price=29.5, currency="USD", image_url="https://picsum.photos/id/23/300/200"),
    Product(id="sku-1004", title="Waveform Wireless Earbuds", description="Crisp sound in a compact form.", price=79.99, currency="USD", image_url="https://picsum.photos/id/24/300/200"),
    Product(id="sku-1005", title="Harbor Travel Mug", description="Insulated mug for hot or cold beverages.", price=24.99, currency="USD", image_url="https://picsum.photos/id/25/300/200"),
    Product(id="sku-1006", title="Tide Performance Tee", description="Breathable tee for everyday comfort.", price=19.99, currency="USD", image_url="https://picsum.photos/id/26/300/200"),
]
