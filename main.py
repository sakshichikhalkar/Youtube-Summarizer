from fastapi import FastAPI
from routes.summarize import router as summarize_router
from database import engine , Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="YouTube Summarizer API",
    description="Summarizes YouTube videos using AI",
    version="1.0.0"
)

app.include_router(summarize_router)

