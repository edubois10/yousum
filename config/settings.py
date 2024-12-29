import os
import yaml

# Load the YAML file
with open('secrets.yaml', 'r') as file:
    config = yaml.safe_load(file)

YOUTUBE_API_KEY = config['youtube_api_key']

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "youtube_data")
DB_USER = os.environ.get("DB_USER", "dbadmin")
DB_PASS = os.environ.get("DB_PASS", "mysecretpassword")
DB_PORT = os.environ.get("DB_PORT", "5432")

LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "http://localhost:60500/v1/chat/completions")
