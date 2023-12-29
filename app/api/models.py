from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.api.db import ReviewStatus


class User(BaseModel):
    id_user: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]


class ReviewIn(BaseModel):
    review_text: str
    rating: float


class ReviewOut(ReviewIn):
    id_review: int
    created_at: datetime
    review_status: ReviewStatus
    fk_user: int
    fk_attraction: int
    user: User
