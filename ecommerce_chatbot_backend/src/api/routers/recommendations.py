"""
Recommendations router.
"""
from fastapi import APIRouter
from ..models import RecommendRequest, RecommendResponse
from ..services import recommend_products

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "",
    summary="Get product recommendations",
    operation_id="recommendations_get",
    response_model=RecommendResponse,
)
def get_recommendations(payload: RecommendRequest):
    """
    Returns a list of recommended products.

    Request body:
        - user_id: optional, reserved for personalization
        - recent_product_ids: optional, signal-based recommendations
        - max_results: max number of items (1-24)

    Returns:
        RecommendResponse with items and rationale string.

    Ocean Professional frontend hint:
        - Render items as cards with soft borders and image thumbnails.
        - Use #2563EB for CTA buttons (e.g., 'Add to Cart') and #F59E0B for badges.
    """
    result = recommend_products(recent_ids=payload.recent_product_ids, max_results=payload.max_results)
    return RecommendResponse(items=result["items"], rationale=result["rationale"])
