from typing import List

from fastapi import APIRouter, HTTPException

from app.api import db_manager
from app.api.db import ReviewStatus
from app.api.models import ReviewIn, ReviewOut, User

review = APIRouter()


@review.get("/", response_model=List[ReviewOut])
async def get_attraction_reviews(id_attraction: int):
    reviews = await db_manager.get_attraction_reviews(id_attraction)
    review_list = []
    for review in reviews:
        user = await db_manager.get_short_user_info(review['fk_user'])
        username = user['email'].split('@')[0]
        review_list.append(ReviewOut(**review,
                                     user=User(
                                         id_user=user['id_user'],
                                         username=username,
                                         first_name=user['first_name'],
                                         last_name=user['last_name'])
                                     )
                           )

    return review_list


@review.post("/")
async def create_attraction_review(id_attraction: int, id_user: int, payload: ReviewIn):
    review_id = await db_manager.add_attraction_review(id_attraction, id_user, payload)
    return {"id_review": review_id,
            "detail": f"Review {review_id} created! Moderation pending"}


@review.put("/{id_review}")
async def update_review_status(id_review: int, status: ReviewStatus):
    try:
        if not await db_manager.get_review(id_review):
            raise Exception('Review does not exist!')
        await db_manager.update_review_status(id_review, status)
        return {"detail": f"Review {id_review} updated! Moderation {status}"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))