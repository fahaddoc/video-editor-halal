"""
Configuration settings for Halal Video Generator
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = BASE_DIR / "templates"

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# Pexels API (Free - get from pexels.com/api)
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# Voice settings (Edge TTS - FREE)
VOICE_SETTINGS = {
    "urdu_male": "ur-PK-AsadNeural",
    "urdu_female": "ur-PK-UzmaNeural",
    "hindi_male": "hi-IN-MadhurNeural",
    "hindi_female": "hi-IN-SwaraNeural",
    "english_male": "en-US-GuyNeural",
    "english_female": "en-US-JennyNeural",
    "arabic_male": "ar-SA-HamedNeural",
    "arabic_female": "ar-SA-ZariyahNeural",
}

# Video settings
VIDEO_SETTINGS = {
    "width": 1920,
    "height": 1080,
    "fps": 24,
    "font_size": 60,
    "font_color": "white",
    "bg_color": "black",
}

# Content categories
CATEGORIES = {
    "1": "Islamic Stories (Sahaba)",
    "2": "Prophet Stories",
    "3": "Quran Lessons",
    "4": "Islamic History",
    "5": "Motivational Islamic",
    "6": "Daily Hadith",
    "7": "Custom Topic",
}
