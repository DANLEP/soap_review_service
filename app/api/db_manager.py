from datetime import datetime

from app.api import gcs
from app.api.db import database, review, ReviewStatus, ReviewStatusExt, photo, PreferenceType, \
    user_attraction_preference
from app.api.models import ReviewIn, ReviewOut, UserExtended, PhotoIn, PhotoOut


async def get_attraction_reviews(id: int, status: ReviewStatus):
    query = review.select((review.c.fk_attraction == id) & (review.c.review_status == status))
    return await database.fetch_all(query=query.order_by(review.c.created_at.desc()))


async def get_reviews(status: ReviewStatusExt):
    if status == ReviewStatusExt.all:
        query = review.select()
    else:
        query = review.select(review.c.review_status == status)
    query = query.order_by(review.c.created_at.desc())
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


async def add_photo(id_review: int, payload: PhotoIn):
    query = photo.insert().values(**payload.dict(), fk_review=id_review, created_at=datetime.utcnow())

    return await database.execute(query=query)


async def get_review_photos(id_review: int):
    query = photo.select(photo.c.fk_review == id_review)
    return await database.fetch_all(query=query)


async def make_preference(id_user: int, id_attraction: int, preference: PreferenceType):
    query = user_attraction_preference.insert().values(
        fk_user=id_user,
        fk_attraction=id_attraction,
        preference_type=preference
    )

    return await database.execute(query=query)


async def extend_review_info(reviews):
    review_list = []

    for review in reviews:
        # add short user info
        user = await get_short_user_info(review['fk_user'])
        username = user['email'].split('@')[0]

        # add photos
        photos = await get_review_photos(review['id_review'])

        list_photos = [PhotoOut(id_photo=photo['id_photo'], created_at=photo['created_at'],
                                url=f"{gcs.google_url}{gcs.bucket_name}/photo/{photo['url']}")
                       for photo in photos]

        # final
        review_list.append(ReviewOut(**review,
                                     user=UserExtended(
                                         id_user=user['id_user'],
                                         username=username,
                                         first_name=user['first_name'],
                                         last_name=user['last_name']),
                                     photos=list_photos
                                     )
                           )

    return review_list
