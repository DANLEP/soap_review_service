from fastapi import APIRouter, HTTPException

from app.api import db_manager
from app.api.models import UserExtended

user = APIRouter()


@user.get("/{id}")
async def get_short_user_info(id: int):
    user = await db_manager.get_short_user_info(id)

    if not user:
        return HTTPException(status_code=404, detail="User not found!")
    return UserExtended(**user)
