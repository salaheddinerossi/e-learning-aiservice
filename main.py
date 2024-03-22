from fastapi import FastAPI
from app.api.endpoints.video_conversion import router as video_conversion_router
from app.api.endpoints.quizz_generator_controller import router as quizz_generator_router
from app.api.endpoints.chat_router import router as chat_router
from app.api.endpoints.correction_router import router as correction_router
from app.api.endpoints.summary_router import router as summary_router

app = FastAPI()

app.include_router(video_conversion_router)
app.include_router(quizz_generator_router)
app.include_router(chat_router)
app.include_router(correction_router)
app.include_router(summary_router)
