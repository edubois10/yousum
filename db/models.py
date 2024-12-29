from db.database import get_db_connection
from psycopg2.extras import RealDictCursor

def get_transcript_by_video_id(video_id):
    """
    Returns the existing record (if any) from youtube_transcripts table
    based on video_id, else returns None.
    """
    query = """
    SELECT id, video_id, title, transcript, summary,
           published_date, channel_name
    FROM youtube_transcripts
    WHERE video_id = %s
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, (video_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def insert_transcript(video_id, title, transcript, summary=None,
                      published_date=None, channel_name=None):
    insert_query = """
    INSERT INTO youtube_transcripts (
        video_id, title, transcript, summary, published_date, channel_name
    ) VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(insert_query, (video_id, title, transcript, summary, published_date, channel_name))
    inserted_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return inserted_id

def update_metadata(record_id, published_date, channel_name):
    """
    Update published_date & channel_name for a given record_id
    """
    update_query = """
    UPDATE youtube_transcripts
    SET published_date = %s, channel_name = %s
    WHERE id = %s
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(update_query, (published_date, channel_name, record_id))
    conn.commit()
    cur.close()
    conn.close()

def get_transcript_record_by_id(record_id):
    query = """
    SELECT id, video_id, title, transcript, summary,
           published_date, channel_name
    FROM youtube_transcripts
    WHERE id = %s
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, (record_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result
