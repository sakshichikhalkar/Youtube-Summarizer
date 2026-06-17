from fastapi import FastAPI

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