# services/api_client.py
import requests
import json
import os

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def download_video(self, url):
        """Mengirim permintaan ke API untuk mendownload video YouTube"""
        try:
            response = requests.post(
                f"{self.base_url}/api/download",
                json={"url": url},
                timeout=600  # Timeout 10 menit untuk download video besar
            )
            
            if response.status_code == 200:
                return True, response.json().get("message", "Success")
            else:
                return False, response.json().get("message", "Unknown error")
        except requests.RequestException as e:
            return False, f"Connection error: {str(e)}"
    
    def split_video(self, video_path, parts, output_dir=None):
        """Mengirim permintaan ke API untuk memotong video"""
        try:
            payload = {
                "video_path": video_path,
                "parts": parts
            }
            
            if output_dir:
                payload["output_dir"] = output_dir
                
            response = requests.post(
                f"{self.base_url}/api/split",
                json=payload,
                timeout=600  # Timeout 10 menit
            )
            
            if response.status_code == 200:
                return True, response.json().get("message", "Success")
            else:
                return False, response.json().get("message", "Unknown error")
        except requests.RequestException as e:
            return False, f"Connection error: {str(e)}"
    
    def get_video_info(self, video_path):
        """Mendapatkan informasi video dari backend"""
        try:
            response = requests.get(
                f"{self.base_url}/api/video_info",
                params={"video_path": video_path},
                timeout=30
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json().get("message", "Unknown error")
        except requests.RequestException as e:
            return False, f"Connection error: {str(e)}"