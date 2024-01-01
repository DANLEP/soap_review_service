import uuid
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, File

from app.api import db_manager
from app.api.db import ReviewStatus, ReviewStatusExt, PreferenceType
from app.api.gcs import upload_to_gcs
from app.api.models import ReviewIn, ReviewOut, PhotoIn

review = APIRouter()


@review.get("/", response_model=List[ReviewOut])
async def get_attraction_reviews(id_attraction: int, status: ReviewStatus = 'approved'):
    reviews = await db_manager.get_attraction_reviews(id_attraction, status)
    return await db_manager.extend_review_info(reviews)


@review.get("/all", response_model=List[ReviewOut])
async def get_reviews(status: ReviewStatusExt = 'all'):
    reviews = await db_manager.get_reviews(status)
    return await db_manager.extend_review_info(reviews)


@review.post("/")
async def create_attraction_review(id_attraction: int,
                                   id_user: int,
                                   payload: ReviewIn):
    review_id = await db_manager.add_attraction_review(id_attraction, id_user, payload)

    return {"id_review": review_id,
            "detail": f"Review {review_id} created! Moderation pending"}


@review.post("/{id_review}/photos")
async def add_photos_to_review(review_id: int, files: List[UploadFile] = File(...)):
    if review_id and files and review_id > 0:
        i = 1
        for file in files:
            if i < 10:
                file.filename = f"{uuid.uuid4()}.jpg"
                public_url = await upload_to_gcs(file)
                photo_id = await db_manager.add_photo(review_id, PhotoIn(url=public_url))
        return {"detail": f"Photos added to review {review_id}!"}
    return {"detail": f"Cant add photo to review {review_id}!"}


@review.put("/{id_review}")
async def update_review_status(id_review: int, status: ReviewStatus):
    try:
        if not await db_manager.get_review(id_review):
            raise Exception('Review does not exist!')
        await db_manager.update_review_status(id_review, status)
        return {"detail": f"Review {id_review} updated! Moderation {status}"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@review.post("/preference/")
async def make_preference(id_user: int, id_attraction, preference: PreferenceType):
    await db_manager.make_preference(id_user, id_attraction, preference)
    return {"detail": "Preference created!"}
