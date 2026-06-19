from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re


def extract_video_id(youtube_url: str) -> str:
    """
    Extracts video ID from any YouTube URL format.
    Handles these formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    """
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:shorts\/)([0-9A-Za-z_-]{11})'
    ]

    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)

    return None


def get_transcript(youtube_url: str) -> dict:
    """
    Takes a YouTube URL and returns clean transcript text.
    """

    # Step 1: Extract video ID
    video_id = extract_video_id(youtube_url)

    if not video_id:
        return {
            "success": False,
            "error": "Invalid YouTube URL. Please check and try again."
        }

    # Step 2: Fetch transcript
    try:
        fetcher = YouTubeTranscriptApi()
        transcript_list = fetcher.fetch(video_id)

        # Step 3: Convert list into one clean string - list comprehension
        full_transcript = " ".join([
            segment.text
            for segment in transcript_list
        ])

        # Step 4: Remove extra whitespace
        full_transcript = " ".join(full_transcript.split())

        return {
            "success": True,
            "transcript": full_transcript,
            "video_id": video_id,
            "word_count": len(full_transcript.split())
        }

    except TranscriptsDisabled:
        return {
            "success": False,
            "error": "This video has transcripts disabled by the creator."
        }

    except NoTranscriptFound:
        return {
            "success": False,
            "error": "No transcript found. Video may not have subtitles."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Something went wrong: {str(e)}"
        }