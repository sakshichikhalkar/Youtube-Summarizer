from fastapi import FastAPI
from services.transcript import get_transcript

app = FastAPI(
    title="YouTube Summarizer API",
    description="Summarizes YouTube videos using AI",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "YouTube Summarizer API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/test-transcript")
def test_transcript(url: str):
    """
    Test endpoint to verify transcript extraction.
    Try it with any YouTube URL.
    """
    result = get_transcript(url)
    return result