from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from services.transcript import get_transcript
from services.summarize import get_summary
from database import get_db
from models import Summary
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.get("/summarize")
@limiter.limit("5/minute")
def summarize_video(request: Request, url: str, summary_type: str = "medium", db: Session = Depends(get_db)):
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


@router.get("/history")
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    """
    Returns the most recent summaries, newest first.
    """
    
    summaries = db.query(Summary).order_by(Summary.created_at.desc()).limit(limit).all()
    
    return {
        "count": len(summaries),
        "results": [
            {
                "id": s.id,
                "video_id": s.video_id,
                "youtube_url": s.youtube_url,
                "summary": s.summary_text,
                "summary_type": s.summary_type,
                "created_at": s.created_at
            }
            for s in summaries
        ]
    }




@router.delete("/summary/{summary_id}")
def delete_summary(summary_id: int, db: Session = Depends(get_db)):
    """
    Deletes a specific summary by its ID.
    """
    
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    
    if not summary:
        return {
            "success": False,
            "error": f"No summary found with id {summary_id}"
        }
    
    db.delete(summary)
    db.commit()
    
    return {
        "success": True,
        "message": f"Summary with id {summary_id} deleted successfully"
    }        