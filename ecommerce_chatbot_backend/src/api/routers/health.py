"""
Health endpoints for readiness and liveness.
"""
from fastapi import APIRouter

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", summary="Health Check", operation_id="health_check")
def health_check():
    """
    Health Check endpoint.

    Use this endpoint for uptime monitoring and CI smoke tests.

    Returns:
        dict: {"message": "Healthy"}
    """
    return {"message": "Healthy"}
