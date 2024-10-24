from typing import Annotated

from fastapi import APIRouter, Body, Depends

from src.services.review import ReviewService
from web.http.v1.dependecies.services import get_review_service
from web.http.v1.routers.review.schemas.body import ReviewBody

review_router = APIRouter()


@review_router.post("/")
async def review_cv(
        body: Annotated[ReviewBody, Body()],
        review_service: Annotated[ReviewService, Depends(get_review_service)]
):
    return await review_service.get_review(
        schema=body
    )
