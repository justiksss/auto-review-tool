from fastapi import APIRouter

from web.http.v1.routers.review.router import review_router

v1_router = APIRouter(prefix="/api/v1")


v1_router.include_router(review_router, prefix="/review", tags=["Review Tool"])
