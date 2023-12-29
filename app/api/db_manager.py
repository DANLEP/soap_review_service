from datetime import datetime

from sqlalchemy import join, select

from app.api.db import database, review, ReviewStatus, user
from app.api.models import ReviewIn


async def get_attraction_reviews(id: int):
    query = review.select(review.c.fk_attraction == id)
    return await database.fetch_all(query=query)


async def get_short_user_info(user_id: int):
    query = f"""
        SELECT id_user, email, first_name, last_name FROM user WHERE id_user = {user_id};
    """

    return await database.fetch_one(query=query)


async def get_review(id_review: int):
    return await database.fetch_one(query=review.select(review.c.id_review == id_review))


async def add_attraction_review(
        id_attraction: int,
        id_user: int,
        payload: ReviewIn):
    query = review.insert().values(
        **payload.dict(),
        fk_user=id_user,
        fk_attraction=id_attraction,
        created_at=datetime.utcnow(),
        review_status=ReviewStatus.pending
    )

    return await database.execute(query=query)


async def update_review_status(id_review: int, status: ReviewStatus):
    query = review.update().where(review.c.id_review == id_review).values(review_status=status)

    return await database.execute(query=query)
