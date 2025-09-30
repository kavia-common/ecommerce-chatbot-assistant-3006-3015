"""
Service layer containing business logic for:
- Chat interactions (mock LLM)
- Product search proxy
- Recommendations engine

Replace mocks with real providers as needed.
"""
from typing import List, Dict, Any, Optional
from .models import Message, Product
from .store import MOCK_PRODUCTS
from .config import get_settings

settings = get_settings()


# PUBLIC_INTERFACE
def generate_chat_reply(messages: List[Message], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Generate a chatbot reply based on messages and optional context.

    This mock implementation simply echoes the user's last message and attempts
    to provide a helpful hint if product-like keywords are detected.

    Returns:
        dict: { "reply": str, "metadata": { "intent": str, ... } }
    """
    last_user = next((m for m in reversed(messages) if m.role == "user"), None)
    user_text = last_user.content if last_user else ""
    # very light intent detection (mock)
    text_low = user_text.lower()
    intent = "smalltalk"
    if any(k in text_low for k in ["recommend", "suggest", "ideas", "gift"]):
        intent = "recommend"
    elif any(k in text_low for k in ["price", "cost", "how much"]):
        intent = "pricing"
    elif any(k in text_low for k in ["return", "refund", "policy"]):
        intent = "policy"
    elif any(k in text_low for k in ["search", "find", "looking for"]):
        intent = "search"

    reply = "Thanks for your message! "
    if intent == "recommend":
        reply += "Would you like some product recommendations? I can suggest popular items."
    elif intent == "pricing":
        reply += "I can help with pricing. Which product are you interested in?"
    elif intent == "policy":
        reply += "Our return policy allows returns within 30 days in original condition."
    elif intent == "search":
        reply += "Tell me what you're looking for and I'll search our catalog."
    else:
        reply += "How can I assist you with our products today?"

    return {
        "reply": reply,
        "metadata": {
            "intent": intent,
            "model": settings.LLM_MODEL,
            "provider": settings.LLM_PROVIDER,
        },
    }


# PUBLIC_INTERFACE
def search_products(query: str, limit: int = 10, filters: Optional[dict] = None) -> List[Product]:
    """
    Search products from the configured provider.

    Mock behavior:
    - Case-insensitive title/description contains query.
    - Filters are ignored in mock but preserved for future use.

    Returns:
        list[Product]: a list of matching products.
    """
    q = query.lower().strip()
    if not q:
        return MOCK_PRODUCTS[:limit]
    res = [
        p for p in MOCK_PRODUCTS
        if q in p.title.lower() or q in p.description.lower()
    ]
    return res[:limit]


# PUBLIC_INTERFACE
def recommend_products(recent_ids: Optional[List[str]] = None, max_results: int = 6) -> Dict[str, Any]:
    """
    Recommend products based on recent interactions or default popularity.

    Mock behavior:
    - If recent_ids present, recommend different items.
    - Otherwise, return top N from catalog.

    Returns:
        dict: { "items": List[Product], "rationale": str }
    """
    if recent_ids:
        pool = [p for p in MOCK_PRODUCTS if p.id not in set(recent_ids)]
        items = pool[:max_results]
        rationale = "Based on your recent views, here are complementary items."
    else:
        items = MOCK_PRODUCTS[:max_results]
        rationale = "Popular items you might like."

    return {"items": items, "rationale": rationale}


# PUBLIC_INTERFACE
def answer_question(question: str, product_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Answer a user question using a simple heuristic (mock).

    - If product_ids provided, tailor the answer mentioning those items.
    - Recognizes basic policy keywords.

    Returns:
        dict: { "answer": str, "related_products": List[str], "confidence": float }
    """
    ql = question.lower()
    related: List[str] = []

    if product_ids:
        related = [pid for pid in product_ids if any(p.id == pid for p in MOCK_PRODUCTS)]

    if "return" in ql or "refund" in ql:
        answer = "We accept returns within 30 days in original condition with receipt."
        conf = 0.9
    elif "shipping" in ql or "deliver" in ql:
        answer = "Standard shipping takes 3-5 business days; expedited options are available at checkout."
        conf = 0.85
    elif "warranty" in ql:
        answer = "Most electronics include a 1-year limited warranty. See product page for details."
        conf = 0.8
    else:
        answer = "Here's what I found based on your question. For specifics, please share more details."
        conf = 0.7

    return {"answer": answer, "related_products": related, "confidence": conf}
