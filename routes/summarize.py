from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.transcript import get_transcript
from services.summarizer import get_summary
from database import get_db
from models import Summary

router = APIRouter()


@router.get("/summarize")
def summarize_video(url: str, summary_type: str = "medium", db: Session = Depends(get_db)):
    """
    Takes a YouTube URL, fetches transcript, 
    returns AI-generated summary, saves it to database.
    """

    transcript_result = get_transcript(url)

    if not transcript_result["success"]:
        return transcript_result

    video_id = transcript_result["video_id"]

    existing = db.query(Summary).filter(
        Summary.video_id == video_id,
        Summary.summary_type == summary_type
    ).first()

    if existing:
        return {
            "video_id": existing.video_id,
            "summary": existing.summary_text,
            "summary_type": existing.summary_type,
            "source": "database (cached)"
        }

    summary_result = get_summary(
        transcript_result["transcript"],
        summary_type
    )

    new_summary = Summary(
        video_id=video_id,
        youtube_url=url,
        summary_text=summary_result["summary"],
        summary_type=summary_type
    )

    db.add(new_summary)
    db.commit()

    return {
        "video_id": video_id,
        "summary": summary_result["summary"],
        "summary_type": summary_type,
        "source": "AI (newly generated)"
    }
        