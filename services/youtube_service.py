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
    
def get_video_id_from_title(title):
    """
    Uses the YouTube Data API to search for a video by title.
    Returns the first matching video's 'videoId', or None if not found.
    """
    if not YOUTUBE_API_KEY or not title:
        return None

    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": title,
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching video ID by title: {e}")
        return None

    data = response.json()
    items = data.get("items", [])
    if not items:
        return None  # No search results

    # Extract the videoId from the first result
    return items[0]["id"]["videoId"]

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
