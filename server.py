from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import requests

app = FastAPI()

# السماح للـ Mini App بالوصول
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# مفتاح YouTube API
YOUTUBE_API_KEY = "AIzaSyDNWF1-aAIueeO6QNbrsarXqNuL0xGJ1ls"

# اختبار السيرفر
@app.get("/")
def home():
    return {"message": "YouTube search server active."}

# البحث بالكلمات المفتاحية
@app.get("/search")
def search_videos(q: str = Query(..., min_length=1), max_results: int = 10):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={q}&key={YOUTUBE_API_KEY}&maxResults={max_results}"
        resp = requests.get(url)
        data = resp.json()
        results = [
            {
                "title": item["snippet"]["title"],
                "video_id": item["id"]["videoId"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            }
            for item in data.get("items", [])
        ]
        return {"status": "ok", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# استخراج رابط صوت MP3 مباشر
@app.get("/audio_url")
def get_audio(video_id: str = Query(...)):
    try:
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {"format": "bestaudio/best", "quiet": True, "noplaylist": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            audio_url = info["url"]
        return {"status": "ok", "audio_url": audio_url}
    except Exception as e:
        return {"status": "error", "message": str(e)}
