from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import instaloader
import json

def extract_video_url(reel_url):
    # Create an instaloader object
    L = instaloader.Instaloader()
    
    # Get the post object from the reel URL
    shortcode = reel_url.split("/")[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    
    if post.is_video:
        return post.video_url
    else:
        raise ValueError("This is not a video post.")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query_params = parse_qs(urlparse(self.path).query)
        url = query_params.get('url', [None])[0]

        # Set response headers
        self.send_response(200 if url else 400)
        self.send_header('Content-Type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")  # Allow requests from any origin
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")  # Allow GET and OPTIONS methods
        self.send_header("Access-Control-Allow-Headers", "Content-Type")  # Allow Content-Type header
        self.end_headers()

        if not url:
            response = {"error": "No URL provided"}
            self.wfile.write(json.dumps(response).encode())
            return

        try:
            video_url = extract_video_url(url)
            response = {"video_url": video_url}
        except Exception as e:
            response = {"error": str(e)}

        self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
