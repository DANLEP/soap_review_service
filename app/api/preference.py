from fastapi import APIRouter

preference = APIRouter()


@preference.get("/")
async def get_preference():
    return {"detail": "Hello World"}
