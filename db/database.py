import psycopg2
from psycopg2.extras import RealDictCursor
from config.settings import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

def create_table_if_not_exists():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS youtube_transcripts (
        id SERIAL PRIMARY KEY,
        video_id VARCHAR(50) NOT NULL,
        title VARCHAR(255),
        transcript TEXT,
        summary TEXT,
        published_date TIMESTAMP,
        channel_name VARCHAR(255)
    );
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()
