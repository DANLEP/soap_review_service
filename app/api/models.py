from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from app.api.db import ReviewStatus


class PhotoIn(BaseModel):
    url: str


class PhotoOut(PhotoIn):
    id_photo: int
    created_at: datetime


class User(BaseModel):
    id_user: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]


class ReviewIn(BaseModel):
    review_text: str
    rating: int


class ReviewOut(ReviewIn):
    id_review: int
    created_at: datetime
    review_status: ReviewStatus
    fk_user: int
    fk_attraction: int
    user: User
    photos: Optional[List[PhotoOut]]
