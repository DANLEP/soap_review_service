from fastapi import APIRouter

from app.api import db_manager
from app.api.db import PreferenceType

preference = APIRouter()


@preference.post("/")
async def make_preference(id_user: int, id_attraction, user_preference: PreferenceType):
    await db_manager.make_preference(id_user, id_attraction, user_preference)
    return {"detail": "Preference created!"}
