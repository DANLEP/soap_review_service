from fastapi import FastAPI

from app.api.user import user
from app.api.db import metadata, engine, database
from app.api.preference import preference
from app.api.review import review

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(review, prefix='/api/v1/review', tags=['review'])
app.include_router(preference, prefix='/api/v1/preference', tags=['preference'])
app.include_router(user, prefix='/api/v1/user', tags=['user'])
