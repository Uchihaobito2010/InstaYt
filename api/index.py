"""
=============================================
APIHut Video Downloader API
Copyright (c) 2024 Paras Chourasiya
Contact Telegram: @Aotpy
=============================================
This software is proprietary and confidential.
Unauthorized copying, distribution, or use is prohibited.
=============================================
"""

import json
import re
import time
import requests
from http.server import BaseHTTPRequestHandler

# Copyright information
COPYRIGHT_INFO = {
    "owner": "Paras Chourasiya",
    "year": 2024,
    "contact": {
        "telegram": "@Aotpy",
        "website": "https://yourwebsite.com"
    },
    "license": "Proprietary Software",
    "notice": "This software is confidential and proprietary.",
    "version": "1.0",
    "api_name": "APIHut Video Downloader"
}

# ==================== UTILITY FUNCTIONS ====================

def add_copyright_to_response(response_data):
    """Add copyright information to response data"""
    if isinstance(response_data, dict):
        response_data['_copyright'] = COPYRIGHT_INFO
    return response_data

def extract_youtube_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/v\/)([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def extract_instagram_media_id(url: str) -> str:
    """Extract Instagram media ID from URL"""
    patterns = [
        r'(?:instagram\.com\/p\/)([a-zA-Z0-9_-]+)',
        r'(?:instagram\.com\/reel\/)([a-zA-Z0-9_-]+)',
        r'(?:instagram\.com\/tv\/)([a-zA-Z0-9_-]+)',
        r'(?:instagram\.com\/reels\/)([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

# ==================== DOWNLOAD FUNCTIONS ====================

def download_youtube_video(url: str) -> dict:
    """Download YouTube video using APIHut"""
    video_id = extract_youtube_video_id(url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    
    api_endpoint = "https://apihut.in/api/download/videos"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://apihut.in",
        "Referer": "https://apihut.in/",
        "Connection": "keep-alive"
    }
    
    payload = {"url": url, "platform": "youtube"}
    
    try:
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return {
            "status": "success",
            "platform": "youtube",
            "video_id": video_id,
            "data": data,
            "timestamp": time.time()
        }
        
    except Exception as e:
        return {"error": f"YouTube download failed: {str(e)}"}

def download_instagram_media(url: str) -> dict:
    """Download Instagram video/reel using APIHut"""
    media_id = extract_instagram_media_id(url)
    if not media_id:
        return {"error": "Invalid Instagram URL"}
    
    api_endpoint = "https://apihut.in/api/download/videos"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://apihut.in",
        "Referer": "https://apihut.in/",
        "Connection": "keep-alive"
    }
    
    payload = {"url": url, "platform": "instagram"}
    
    try:
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return {
            "status": "success",
            "platform": "instagram",
            "media_id": media_id,
            "data": data,
            "timestamp": time.time()
        }
        
    except Exception as e:
        return {"error": f"Instagram download failed: {str(e)}"}

# ==================== HTTP HANDLER FOR VERCEL ====================

class handler(BaseHTTPRequestHandler):
    
    def set_headers(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self.set_headers(200)
    
    def do_GET(self):
        path = self.path.split('?')[0]
        
        if path == '/':
            self.home()
        elif path == '/copyright':
            self.copyright()
        elif path == '/status':
            self.status()
        else:
            self.not_found()
    
    def do_POST(self):
        path = self.path.split('?')[0]
        
        if path == '/download':
            self.handle_download()
        elif path == '/youtube':
            self.handle_youtube()
        elif path == '/instagram':
            self.handle_instagram()
        else:
            self.not_found()
    
    def home(self):
        """API Homepage"""
        info_response = {
            "api_name": "APIHut Video Downloader API",
            "version": "1.0",
            "developer": "Paras Chourasiya",
            "contact": "@Aotpy (Telegram)",
            "endpoints": {
                "POST /download": "Download video (auto-detect)",
                "POST /youtube": "Download YouTube video",
                "POST /instagram": "Download Instagram video/reel",
                "GET /copyright": "Copyright information",
                "GET /status": "API status"
            },
            "example": {
                "curl": 'curl -X POST "https://your-app.vercel.app/download" -H "Content-Type: application/json" -d \'{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}\''
            }
        }
        
        info_response = add_copyright_to_response(info_response)
        self.set_headers(200)
        self.wfile.write(json.dumps(info_response, indent=2).encode())
    
    def copyright(self):
        """Copyright information"""
        response = {"_copyright": COPYRIGHT_INFO}
        self.set_headers(200)
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def status(self):
        """API Status"""
        response = {
            "status": "online",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "platforms": ["youtube", "instagram"]
        }
        response = add_copyright_to_response(response)
        self.set_headers(200)
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def handle_download(self):
        """Handle /download endpoint"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error_response("No data received", 400)
                return
            
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            url = data.get('url')
            platform = data.get('platform', 'auto')
            
            if not url:
                self.send_error_response("URL parameter is required", 400)
                return
            
            # Auto-detect platform
            if platform == 'auto':
                if 'youtube.com' in url or 'youtu.be' in url:
                    platform = 'youtube'
                elif 'instagram.com' in url:
                    platform = 'instagram'
                else:
                    self.send_error_response("Unsupported platform", 400)
                    return
            
            # Download based on platform
            if platform == 'youtube':
                result = download_youtube_video(url)
            elif platform == 'instagram':
                result = download_instagram_media(url)
            else:
                self.send_error_response(f"Unsupported platform: {platform}", 400)
                return
            
            if "error" in result:
                self.send_error_response(result["error"], 500)
                return
            
            # Add metadata
            result["api_credit"] = "@Aotpy"
            result["developer"] = "Paras Chourasiya"
            result = add_copyright_to_response(result)
            
            self.set_headers(200)
            self.wfile.write(json.dumps(result, indent=2).encode())
            
        except json.JSONDecodeError:
            self.send_error_response("Invalid JSON data", 400)
        except Exception as e:
            self.send_error_response(f"Server error: {str(e)}", 500)
    
    def handle_youtube(self):
        """Handle /youtube endpoint"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error_response("No data received", 400)
                return
            
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            url = data.get('url')
            if not url:
                self.send_error_response("URL parameter is required", 400)
                return
            
            result = download_youtube_video(url)
            
            if "error" in result:
                self.send_error_response(result["error"], 500)
                return
            
            result["api_credit"] = "@Aotpy"
            result["developer"] = "Paras Chourasiya"
            result = add_copyright_to_response(result)
            
            self.set_headers(200)
            self.wfile.write(json.dumps(result, indent=2).encode())
            
        except Exception as e:
            self.send_error_response(f"YouTube error: {str(e)}", 500)
    
    def handle_instagram(self):
        """Handle /instagram endpoint"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error_response("No data received", 400)
                return
            
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            url = data.get('url')
            if not url:
                self.send_error_response("URL parameter is required", 400)
                return
            
            result = download_instagram_media(url)
            
            if "error" in result:
                self.send_error_response(result["error"], 500)
                return
            
            result["api_credit"] = "apihut.in"
            result["developer"] = "Paras Chourasiya"
            result = add_copyright_to_response(result)
            
            self.set_headers(200)
            self.wfile.write(json.dumps(result, indent=2).encode())
            
        except Exception as e:
            self.send_error_response(f"Instagram error: {str(e)}", 500)
    
    def send_error_response(self, message, status_code):
        error_response = {
            "status": "error",
            "message": message,
            "timestamp": time.time()
        }
        error_response = add_copyright_to_response(error_response)
        
        self.set_headers(status_code)
        self.wfile.write(json.dumps(error_response, indent=2).encode())
    
    def not_found(self):
        error_response = {
            "status": "error",
            "message": "Endpoint not found",
            "available_endpoints": [
                "GET /",
                "POST /download",
                "POST /youtube", 
                "POST /instagram",
                "GET /copyright",
                "GET /status"
            ]
        }
        error_response = add_copyright_to_response(error_response)
        
        self.set_headers(404)
        self.wfile.write(json.dumps(error_response, indent=2).encode())

# This is required for Vercel
if __name__ == "__main__":
    print("APIHut Video Downloader API - Running on Vercel")
