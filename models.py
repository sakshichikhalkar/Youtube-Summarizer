from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, index=True)
    youtube_url = Column(String)
    summary_text = Column(Text)
    summary_type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    