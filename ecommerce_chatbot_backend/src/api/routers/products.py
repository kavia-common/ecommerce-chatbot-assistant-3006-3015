"""
Products router: search and lookup endpoints.
"""
from fastapi import APIRouter, HTTPException
from ..models import ProductSearchRequest, ProductSearchResponse, Product
from ..services import search_products
from ..store import MOCK_PRODUCTS

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "/search",
    summary="Search products",
    operation_id="products_search",
    response_model=ProductSearchResponse,
)
def products_search(payload: ProductSearchRequest):
    """
    Search products with an optional filter set.

    Request body:
        - query: text to search in title and description
        - limit: max number of items to return (1-50)
        - filters: optional filters for future provider support

    Returns:
        ProductSearchResponse: items and total count (mock).
    """
    items = search_products(payload.query, limit=payload.limit, filters=payload.filters)
    return ProductSearchResponse(items=items, total=len(items))


# PUBLIC_INTERFACE
@router.get(
    "/{product_id}",
    summary="Get product detail",
    operation_id="products_get",
    response_model=Product,
    responses={404: {"description": "Product not found"}},
)
def get_product(product_id: str):
    """
    Retrieve a single product by ID.

    Path params:
        - product_id: the product's unique identifier

    Returns:
        Product model

    Raises:
        404 if product is not found.
    """
    item = next((p for p in MOCK_PRODUCTS if p.id == product_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    return item
