"""
Caption Visuals System
AI Image Generation + Stock Search + Manual Upload
For per-caption background images
"""
import os
import re
import json
import hashlib
import requests
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO
from typing import Optional, List, Dict
import urllib.parse

# Cache directory for generated/downloaded images
CACHE_DIR = Path(__file__).parent.parent / "assets" / "caption_images"
CACHE_DIR.mkdir(exist_ok=True)


class CaptionVisuals:
    """Manages visuals for each caption - AI generation, stock search, uploads"""

    def __init__(self):
        self.cache = {}
        self._load_cache()

    def _load_cache(self):
        """Load cached image mappings"""
        cache_file = CACHE_DIR / "cache.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    self.cache = json.load(f)
            except:
                self.cache = {}

    def _save_cache(self):
        """Save cache mappings"""
        cache_file = CACHE_DIR / "cache.json"
        with open(cache_file, 'w') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _get_cache_key(self, text: str) -> str:
        """Generate cache key from text"""
        return hashlib.md5(text.encode()).hexdigest()[:12]

    # ============ AI IMAGE GENERATION ============

    def generate_ai_image(self, prompt: str, style: str = "cinematic") -> Optional[Path]:
        """
        Generate image using free AI API (Pollinations.ai)

        Args:
            prompt: Description of image to generate
            style: Art style - cinematic, anime, realistic, dark, etc.

        Returns:
            Path to generated image or None
        """
        cache_key = self._get_cache_key(f"ai_{prompt}_{style}")
        cached_path = CACHE_DIR / f"{cache_key}.png"

        if cached_path.exists():
            return cached_path

        try:
            import time

            # Enhance prompt for better results
            enhanced_prompt = self._enhance_prompt(prompt, style)

            # Use Pollinations.ai (free, no API key needed)
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"

            # Retry with delay for rate limiting
            max_retries = 3
            for attempt in range(max_retries):
                response = requests.get(url, timeout=90)

                if response.status_code == 429:  # Rate limited
                    print(f"Rate limited, waiting 10 seconds... (attempt {attempt+1}/{max_retries})")
                    time.sleep(10)
                    continue
                break

            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img = img.convert('RGB')
                img.save(cached_path, 'PNG')

                self.cache[cache_key] = {
                    'type': 'ai',
                    'prompt': prompt,
                    'style': style,
                    'path': str(cached_path)
                }
                self._save_cache()

                return cached_path
        except Exception as e:
            print(f"AI generation error: {e}")

        return None

    def _enhance_prompt(self, prompt: str, style: str) -> str:
        """Enhance prompt for better AI results"""
        style_modifiers = {
            'cinematic': 'cinematic lighting, dramatic, movie scene, high quality',
            'dark': 'dark atmosphere, moody, shadows, horror aesthetic, eerie',
            'anime': 'anime style, vibrant colors, detailed illustration',
            'realistic': 'photorealistic, 4k, detailed, professional photography',
            'fantasy': 'fantasy art, magical, ethereal, mystical atmosphere',
            'minimal': 'minimalist, clean, simple background, elegant',
        }

        modifier = style_modifiers.get(style, style_modifiers['cinematic'])

        # Translate common Urdu keywords to English for better AI understanding
        urdu_to_english = {
            'سایہ': 'shadow figure, silhouette',
            'رات': 'night, darkness',
            'چاند': 'moon, moonlight',
            'گھر': 'house, home',
            'اندھیرا': 'darkness, dark room',
            'خوف': 'fear, scary',
            'روشنی': 'light, glow',
            'جنگل': 'forest, trees',
            'پہاڑ': 'mountains',
            'سمندر': 'ocean, sea',
            'آسمان': 'sky',
            'ستارے': 'stars',
            'بارش': 'rain',
            'دروازہ': 'door, doorway',
            'کھڑکی': 'window',
            'آنکھیں': 'eyes',
            'ہاتھ': 'hands',
        }

        enhanced = prompt
        for urdu, english in urdu_to_english.items():
            if urdu in enhanced:
                enhanced = enhanced.replace(urdu, f'{urdu} ({english})')

        return f"{enhanced}, {modifier}"

    # ============ STOCK IMAGE SEARCH ============

    def search_stock_images(self, query: str, count: int = 5) -> List[Dict]:
        """
        Search free stock images from Unsplash

        Args:
            query: Search keywords
            count: Number of results

        Returns:
            List of image info dicts with urls
        """
        results = []

        try:
            # Use Unsplash Source (no API key needed for basic use)
            # Extract English keywords from Urdu text
            keywords = self._extract_keywords(query)

            for i in range(count):
                # Generate different variations
                search_term = urllib.parse.quote(keywords)
                url = f"https://source.unsplash.com/1280x720/?{search_term}&sig={i}"

                results.append({
                    'url': url,
                    'query': keywords,
                    'source': 'unsplash',
                    'index': i
                })
        except Exception as e:
            print(f"Stock search error: {e}")

        return results

    def download_stock_image(self, url: str, caption_text: str) -> Optional[Path]:
        """Download and cache a stock image"""
        cache_key = self._get_cache_key(f"stock_{url}")
        cached_path = CACHE_DIR / f"{cache_key}.jpg"

        if cached_path.exists():
            return cached_path

        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img = img.convert('RGB')
                img.save(cached_path, 'JPEG', quality=90)

                self.cache[cache_key] = {
                    'type': 'stock',
                    'url': url,
                    'caption': caption_text,
                    'path': str(cached_path)
                }
                self._save_cache()

                return cached_path
        except Exception as e:
            print(f"Download error: {e}")

        return None

    def _extract_keywords(self, text: str) -> str:
        """Extract English keywords from Urdu/mixed text"""
        # Urdu to English keyword mapping for stock search
        keyword_map = {
            'رات': 'night dark',
            'سایہ': 'shadow silhouette',
            'گھر': 'house building',
            'ویران': 'abandoned empty',
            'خوفناک': 'scary horror',
            'چاند': 'moon night',
            'اندھیرا': 'darkness',
            'کمرہ': 'room interior',
            'دروازہ': 'door',
            'کھڑکی': 'window',
            'جنگل': 'forest trees',
            'قبرستان': 'graveyard cemetery',
            'بستر': 'bed bedroom',
            'آنکھ': 'eye eyes',
            'سیاہ': 'black dark',
            'سرگوشی': 'whisper mystery',
            'مسجد': 'mosque islamic',
            'نماز': 'prayer spiritual',
            'قرآن': 'quran book',
        }

        keywords = []
        for urdu, english in keyword_map.items():
            if urdu in text:
                keywords.append(english)

        if not keywords:
            keywords = ['abstract background']

        return ' '.join(keywords[:3])  # Limit to 3 keyword phrases

    # ============ MANUAL UPLOAD ============

    def save_uploaded_image(self, image_data: bytes, caption_text: str) -> Path:
        """Save an uploaded image for a caption"""
        cache_key = self._get_cache_key(f"upload_{caption_text}")
        save_path = CACHE_DIR / f"{cache_key}.png"

        img = Image.open(BytesIO(image_data))
        img = img.convert('RGB')

        # Resize to video dimensions
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        img.save(save_path, 'PNG')

        self.cache[cache_key] = {
            'type': 'upload',
            'caption': caption_text,
            'path': str(save_path)
        }
        self._save_cache()

        return save_path

    # ============ IMAGE PROCESSING ============

    def prepare_for_video(self, image_path: Path, width: int = 1920, height: int = 1080,
                         darken: float = 0.4, blur: int = 0) -> Image.Image:
        """
        Prepare image for video background

        Args:
            image_path: Path to source image
            width, height: Target dimensions
            darken: Darken factor (0=black, 1=original)
            blur: Blur radius (0=none)

        Returns:
            Processed PIL Image
        """
        img = Image.open(image_path).convert('RGBA')

        # Resize to cover
        img_ratio = img.width / img.height
        target_ratio = width / height

        if img_ratio > target_ratio:
            new_height = height
            new_width = int(height * img_ratio)
        else:
            new_width = width
            new_height = int(width / img_ratio)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Center crop
        left = (new_width - width) // 2
        top = (new_height - height) // 2
        img = img.crop((left, top, left + width, top + height))

        # Apply blur if specified
        if blur > 0:
            img = img.filter(ImageFilter.GaussianBlur(blur))

        # Darken for text readability
        if darken < 1:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(darken)

        return img

    # ============ BATCH OPERATIONS ============

    def generate_all_visuals(self, captions: List[str], style: str = "cinematic",
                            mode: str = "ai", progress_callback=None) -> Dict[int, Path]:
        """
        Generate visuals for all captions

        Args:
            captions: List of caption texts
            style: Visual style
            mode: 'ai', 'stock', or 'both'
            progress_callback: Progress update function

        Returns:
            Dict mapping caption index to image path
        """
        visuals = {}
        total = len(captions)

        for i, caption in enumerate(captions):
            if progress_callback:
                progress_callback(int(100 * i / total), f"Generating visual {i+1}/{total}")

            image_path = None

            if mode in ['ai', 'both']:
                image_path = self.generate_ai_image(caption, style)

            if image_path is None and mode in ['stock', 'both']:
                stock_results = self.search_stock_images(caption, 1)
                if stock_results:
                    image_path = self.download_stock_image(stock_results[0]['url'], caption)

            if image_path:
                visuals[i] = image_path

        if progress_callback:
            progress_callback(100, "Visuals ready!")

        return visuals


# Singleton instance
_caption_visuals = None

def get_caption_visuals() -> CaptionVisuals:
    """Get singleton instance"""
    global _caption_visuals
    if _caption_visuals is None:
        _caption_visuals = CaptionVisuals()
    return _caption_visuals


# Quick test
if __name__ == "__main__":
    cv = CaptionVisuals()

    # Test AI generation
    print("Testing AI image generation...")
    path = cv.generate_ai_image("dark shadow in bedroom at night", "dark")
    print(f"Generated: {path}")

    # Test stock search
    print("\nTesting stock search...")
    results = cv.search_stock_images("رات کا اندھیرا")
    print(f"Found {len(results)} results")
