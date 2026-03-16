"""
Stock Footage Module
Downloads free stock videos and images from Pexels
"""
import os
import requests
from pathlib import Path
from typing import List, Optional
from config import PEXELS_API_KEY, ASSETS_DIR


class PexelsDownloader:
    """Download stock footage from Pexels (FREE API)"""

    BASE_URL = "https://api.pexels.com"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or PEXELS_API_KEY
        self.headers = {"Authorization": self.api_key}

    def search_videos(
        self,
        query: str,
        per_page: int = 10,
        orientation: str = "landscape"
    ) -> List[dict]:
        """
        Search for videos on Pexels

        Args:
            query: Search term
            per_page: Number of results
            orientation: landscape, portrait, or square

        Returns:
            List of video data dictionaries
        """
        if not self.api_key:
            print("Warning: No Pexels API key. Using fallback images.")
            return []

        url = f"{self.BASE_URL}/videos/search"
        params = {
            "query": query,
            "per_page": per_page,
            "orientation": orientation,
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("videos", [])
        except Exception as e:
            print(f"Error searching videos: {e}")
            return []

    def search_images(
        self,
        query: str,
        per_page: int = 10,
        orientation: str = "landscape"
    ) -> List[dict]:
        """Search for images on Pexels"""
        if not self.api_key:
            return []

        url = f"{self.BASE_URL}/v1/search"
        params = {
            "query": query,
            "per_page": per_page,
            "orientation": orientation,
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("photos", [])
        except Exception as e:
            print(f"Error searching images: {e}")
            return []

    def download_video(
        self,
        video_data: dict,
        output_dir: Path = None,
        quality: str = "hd"
    ) -> Optional[Path]:
        """
        Download a video from Pexels

        Args:
            video_data: Video data from search results
            output_dir: Where to save
            quality: 'hd', 'sd', or 'hls'

        Returns:
            Path to downloaded video
        """
        output_dir = output_dir or ASSETS_DIR

        try:
            video_files = video_data.get("video_files", [])

            # Find desired quality
            video_url = None
            for vf in video_files:
                if quality in vf.get("quality", "").lower():
                    video_url = vf.get("link")
                    break

            # Fallback to first available
            if not video_url and video_files:
                video_url = video_files[0].get("link")

            if not video_url:
                return None

            # Download
            filename = f"video_{video_data.get('id', 'unknown')}.mp4"
            output_path = output_dir / filename

            response = requests.get(video_url, stream=True)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return output_path

        except Exception as e:
            print(f"Error downloading video: {e}")
            return None

    def download_image(
        self,
        image_data: dict,
        output_dir: Path = None,
        size: str = "large"
    ) -> Optional[Path]:
        """Download an image from Pexels"""
        output_dir = output_dir or ASSETS_DIR

        try:
            src = image_data.get("src", {})
            image_url = src.get(size) or src.get("original")

            if not image_url:
                return None

            filename = f"image_{image_data.get('id', 'unknown')}.jpg"
            output_path = output_dir / filename

            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return output_path

        except Exception as e:
            print(f"Error downloading image: {e}")
            return None


def get_islamic_stock_queries() -> dict:
    """
    Returns suggested search queries for Islamic content
    """
    return {
        "general": [
            "mosque",
            "islamic architecture",
            "quran",
            "prayer",
            "meditation peaceful",
            "sky clouds",
            "nature peaceful",
            "sunrise",
            "sunset",
            "stars night sky",
        ],
        "emotional": [
            "person praying",
            "peaceful nature",
            "ocean waves",
            "rain",
            "mountains",
            "forest peaceful",
        ],
        "historical": [
            "desert",
            "arabian desert",
            "middle east architecture",
            "ancient buildings",
            "sand dunes",
        ],
        "motivational": [
            "sunrise hope",
            "mountain climbing",
            "success",
            "light through darkness",
            "road journey",
        ],
    }


def download_footage_for_script(
    script_type: str,
    downloader: PexelsDownloader,
    num_clips: int = 5
) -> List[Path]:
    """
    Download appropriate footage based on script type

    Args:
        script_type: Type of content (sahaba, prophets, etc.)
        downloader: PexelsDownloader instance
        num_clips: Number of clips to download

    Returns:
        List of paths to downloaded footage
    """
    queries = get_islamic_stock_queries()

    # Select appropriate queries based on script type
    if script_type in ["sahaba", "prophets", "historical"]:
        search_terms = queries["historical"] + queries["general"][:3]
    elif script_type == "motivational":
        search_terms = queries["motivational"] + queries["emotional"][:3]
    else:
        search_terms = queries["general"]

    downloaded = []

    for term in search_terms[:num_clips]:
        # Try videos first
        videos = downloader.search_videos(term, per_page=1)
        if videos:
            path = downloader.download_video(videos[0])
            if path:
                downloaded.append(path)
                continue

        # Fallback to images
        images = downloader.search_images(term, per_page=1)
        if images:
            path = downloader.download_image(images[0])
            if path:
                downloaded.append(path)

    return downloaded


# Fallback: Create simple background images without API
def create_fallback_backgrounds(output_dir: Path, count: int = 5) -> List[Path]:
    """
    Create simple gradient backgrounds when no API key available
    """
    try:
        from PIL import Image, ImageDraw

        backgrounds = []
        colors = [
            [(20, 30, 48), (36, 59, 85)],      # Dark blue
            [(15, 32, 39), (32, 58, 67)],      # Dark teal
            [(44, 62, 80), (52, 73, 94)],      # Slate
            [(25, 25, 35), (45, 45, 65)],      # Dark purple
            [(30, 30, 30), (50, 50, 50)],      # Dark gray
        ]

        for i, (color1, color2) in enumerate(colors[:count]):
            img = Image.new('RGB', (1920, 1080))
            draw = ImageDraw.Draw(img)

            # Create gradient
            for y in range(1080):
                r = int(color1[0] + (color2[0] - color1[0]) * y / 1080)
                g = int(color1[1] + (color2[1] - color1[1]) * y / 1080)
                b = int(color1[2] + (color2[2] - color1[2]) * y / 1080)
                draw.line([(0, y), (1920, y)], fill=(r, g, b))

            path = output_dir / f"background_{i+1}.png"
            img.save(path)
            backgrounds.append(path)

        return backgrounds

    except ImportError:
        print("Pillow not installed. Cannot create fallback backgrounds.")
        return []
