from fastapi import FastAPI
from app.api.endpoints.video_conversion import router as video_conversion_router

app = FastAPI()

app.include_router(video_conversion_router)
