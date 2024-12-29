from youtube_transcript_api import YouTubeTranscriptApi
import requests
from datetime import datetime
from config.settings import YOUTUBE_API_KEY

def fetch_youtube_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([x['text'] for x in transcript_list])
        return transcript_text
    except Exception as e:
        # You might want to raise or handle the exception
        raise RuntimeError(f"Could not retrieve transcript: {str(e)}")

def get_video_metadata(video_id):
    """
    Fetch published date and channel name via the YouTube Data API (v3).
    Returns (published_date, channel_name) or (None, None) if not found.
    """
    if not YOUTUBE_API_KEY:
        return None, None
    
    url = (
        "https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception:
        return None, None

    data = response.json()
    items = data.get("items", [])
    if not items:
        return None, None

    snippet = items[0].get("snippet", {})
    published_at = snippet.get("publishedAt")     # e.g. 2023-09-03T12:34:56Z
    channel_name = snippet.get("channelTitle")

    if published_at:
        published_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
    else:
        published_date = None

    return published_date, channel_name
