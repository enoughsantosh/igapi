from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import instaloader
from vercel_fastapi import VercelMiddleware  # Required for Vercel

app = FastAPI()
app.add_middleware(VercelMiddleware)  # Vercel middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_video_url(reel_url: str):
    try:
        L = instaloader.Instaloader()
        shortcode = reel_url.split("/")[-2]  # Extract shortcode from URL
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        if post.is_video:
            return post.video_url
        else:
            return None
    except Exception as e:
        raise ValueError(f"Failed to fetch video: {str(e)}")

@app.get("/download")
async def download_reel(url: str = Query(..., description="Instagram reel URL")):
    try:
        video_url = extract_video_url(url)
        if video_url:
            return {"video_url": video_url}
        else:
            return {"error": "This is not a video post."}
    except Exception as e:
        return {"error": str(e)}
