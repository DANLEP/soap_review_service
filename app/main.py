from fastapi import FastAPI

from app.api.db import metadata, engine, database
from app.api.review import review

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/review/openapi.json", docs_url="/api/v1/review/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(review, prefix='/api/v1/review', tags=['review'])