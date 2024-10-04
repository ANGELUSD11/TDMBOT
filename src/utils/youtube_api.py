# utils/youtube_api.py
from googleapiclient.discovery import build

def build_youtube_service(api_key):
    return build('youtube', 'v3', developerKey=api_key)