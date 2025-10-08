from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build

app = FastAPI()

# السماح بالوصول من أي مصدر (لأن الميني أب يحتاجه)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

YOUTUBE_API_KEY = "AIzaSyDNWF1-aAIueeO6QNbrsarXqNuL0xGJ1ls"

@app.get("/")
def home():
    return {"message": "YouTube search server active."}

@app.get("/search")
def search_videos(q: str = Query(..., min_length=1)):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=q,
        part="snippet",
        type="video",
        maxResults=10
    )
    response = request.execute()
    results = [
        {
            "title": item["snippet"]["title"],
            "videoId": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
        }
        for item in response["items"]
    ]
    return {"results": results}
