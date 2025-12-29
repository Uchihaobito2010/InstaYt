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
import os
import re
import time
import requests

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

# ==================== HELPER FUNCTIONS ====================

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

def download_from_apihut(url: str, platform: str) -> dict:
    """Download video using APIHut"""
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
    
    payload = {"url": url, "platform": platform}
    
    try:
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if platform == "youtube":
            video_id = extract_youtube_video_id(url)
            return {
                "status": "success",
                "platform": "youtube",
                "video_id": video_id,
                "data": data,
                "timestamp": time.time()
            }
        elif platform == "instagram":
            media_id = extract_instagram_media_id(url)
            return {
                "status": "success",
                "platform": "instagram",
                "media_id": media_id,
                "data": data,
                "timestamp": time.time()
            }
        
    except Exception as e:
        return {"error": f"Download failed: {str(e)}"}

# ==================== VERCEL HANDLER ====================

def handler(request):
    """Main Vercel serverless function handler"""
    
    # Set CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle OPTIONS request for CORS
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    path = request.path
    method = request.method
    
    try:
        # GET /
        if method == 'GET' and path == '/':
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
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(info_response, indent=2)
            }
        
        # GET /copyright
        elif method == 'GET' and path == '/copyright':
            response = {"_copyright": COPYRIGHT_INFO}
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response, indent=2)
            }
        
        # GET /status
        elif method == 'GET' and path == '/status':
            response = {
                "status": "online",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "platforms": ["youtube", "instagram"]
            }
            response = add_copyright_to_response(response)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response, indent=2)
            }
        
        # POST endpoints
        elif method == 'POST':
            # Parse request body
            if not request.body:
                error_response = {
                    "status": "error",
                    "message": "No data received"
                }
                error_response = add_copyright_to_response(error_response)
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps(error_response, indent=2)
                }
            
            try:
                data = json.loads(request.body)
            except:
                error_response = {
                    "status": "error",
                    "message": "Invalid JSON data"
                }
                error_response = add_copyright_to_response(error_response)
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps(error_response, indent=2)
                }
            
            url = data.get('url')
            
            if not url:
                error_response = {
                    "status": "error",
                    "message": "URL parameter is required"
                }
                error_response = add_copyright_to_response(error_response)
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps(error_response, indent=2)
                }
            
            # POST /download
            if path == '/download':
                platform = data.get('platform', 'auto')
                
                if platform == 'auto':
                    if 'youtube.com' in url or 'youtu.be' in url:
                        platform = 'youtube'
                    elif 'instagram.com' in url:
                        platform = 'instagram'
                    else:
                        error_response = {
                            "status": "error",
                            "message": "Unsupported platform. Please specify 'youtube' or 'instagram'"
                        }
                        error_response = add_copyright_to_response(error_response)
                        return {
                            'statusCode': 400,
                            'headers': headers,
                            'body': json.dumps(error_response, indent=2)
                        }
                
                result = download_from_apihut(url, platform)
            
            # POST /youtube
            elif path == '/youtube':
                result = download_from_apihut(url, 'youtube')
            
            # POST /instagram
            elif path == '/instagram':
                result = download_from_apihut(url, 'instagram')
            
            else:
                error_response = {
                    "status": "error",
                    "message": "Endpoint not found"
                }
                error_response = add_copyright_to_response(error_response)
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps(error_response, indent=2)
                }
            
            if "error" in result:
                error_response = {
                    "status": "error",
                    "message": result["error"]
                }
                error_response = add_copyright_to_response(error_response)
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps(error_response, indent=2)
                }
            
            # Add metadata and copyright
            result["api_credit"] = "apihut.in"
            result["developer"] = "Paras Chourasiya"
            result = add_copyright_to_response(result)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result, indent=2)
            }
        
        # 404 Not Found
        else:
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
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps(error_response, indent=2)
            }
    
    except Exception as e:
        error_response = {
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }
        error_response = add_copyright_to_response(error_response)
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(error_response, indent=2)
        }

# For local testing
if __name__ == "__main__":
    # Simulate a request for testing
    class MockRequest:
        def __init__(self, method="GET", path="/", body=None):
            self.method = method
            self.path = path
            self.body = body
    
    # Test the handler
    test_request = MockRequest(method="GET", path="/")
    response = handler(test_request)
    print("Test Response:", json.dumps(response, indent=2))
