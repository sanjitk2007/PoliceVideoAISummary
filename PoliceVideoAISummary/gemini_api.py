import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=${GEMINI_API_KEY}'

PROMPT = "You are a helpful police assistant. Summarize the key events in this video clip for an incident report. Be objective and concise. List the events chronologically."

def summarize_video_chunk(chunk_path):
    with open(chunk_path, 'rb') as f:
        files = {
            'file': (os.path.basename(chunk_path), f, 'video/mp4')
        }
        data = {
            'prompt': PROMPT
        }
        response = requests.post(GEMINI_API_URL, files=files, data=data)
        if response.status_code == 200:
            return response.json().get('summary', '')
        else:
            raise Exception(f"Gemini API error: {response.text}") 