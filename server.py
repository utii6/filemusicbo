from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import requests

app = FastAPI()

YOUTUBE_API_KEY = "AIzaSyDNWF1-aAIueeO6QNbrsarXqNuL0xGJ1ls"

# البحث بالكلمات المفتاحية
@app.get("/search")
def search_videos(q: str = Query(...), max_results: int = 10):
    try:
        url = (
            f"https://www.googleapis.com/youtube/v3/search"
            f"?part=snippet&type=video&q={q}&key={YOUTUBE_API_KEY}&maxResults={max_results}"
        )
        resp = requests.get(url)
        data = resp.json()
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item["snippet"]["title"],
                "video_id": item["id"]["videoId"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            })
        return {"status": "ok", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# استخراج رابط صوت MP3 للفيديو
@app.get("/audio_url")
def get_audio(video_id: str = Query(...)):
    try:
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": True,
            "extract_flat": False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            audio_url = info["url"]
            title = info.get("title")
            thumbnail = info.get("thumbnail")
            return JSONResponse({
                "status": "ok",
                "title": title,
                "thumbnail": thumbnail,
                "audio_url": audio_url
            })
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})
