"""
Video Creator for Urdu/Arabic Content
Handles RTL text and Arabic script display
"""
import os
import math
import subprocess
from pathlib import Path
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from moviepy import (
    VideoFileClip,
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ColorClip,
)

from config import VIDEO_SETTINGS, OUTPUT_DIR, ASSETS_DIR


# Arabic-supporting fonts on macOS
ARABIC_FONTS = [
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/GeezaPro.ttc",
    "/System/Library/Fonts/Supplemental/Geeza Pro.ttf",
    "/System/Library/Fonts/Supplemental/Al Nile.ttf",
]


def get_arabic_font(size: int = 48):
    """Get a font that supports Arabic/Urdu text"""
    for font_path in ARABIC_FONTS:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue

    # Fallback to default
    return ImageFont.load_default()


class UrduVideoCreator:
    """Creates videos with Urdu/Arabic text support"""

    def __init__(self):
        self.width = VIDEO_SETTINGS["width"]
        self.height = VIDEO_SETTINGS["height"]
        self.fps = VIDEO_SETTINGS["fps"]

    def create_video(
        self,
        audio_path: Path,
        script_data: dict,
        output_path: Path = None,
        bg_style: str = "starfield"
    ) -> Path:
        """
        Create complete video with Urdu/Arabic text

        Args:
            audio_path: Path to voiceover audio
            script_data: Dict containing title, arabic_ayat, subtitle_lines
            output_path: Where to save final video
            bg_style: Background style (starfield, particles, gradient)
        """
        output_path = output_path or OUTPUT_DIR / "urdu_video.mp4"

        # Load audio
        audio = AudioFileClip(str(audio_path))
        total_duration = audio.duration

        print(f"Creating video ({total_duration:.0f}s)...")

        # Create frames with text overlays
        frames_dir = ASSETS_DIR / "video_frames"
        frames_dir.mkdir(exist_ok=True)

        self._create_video_frames(
            frames_dir=frames_dir,
            duration=total_duration,
            script_data=script_data,
            bg_style=bg_style
        )

        # Compile frames to video
        print("Compiling video...")
        temp_video = ASSETS_DIR / "temp_video.mp4"

        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(self.fps),
            "-i", str(frames_dir / "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "20",
            str(temp_video)
        ]
        subprocess.run(cmd, capture_output=True)

        # Add audio
        print("Adding audio...")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(temp_video),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(output_path)
        ]
        subprocess.run(cmd, capture_output=True)

        # Cleanup
        print("Cleaning up...")
        for f in frames_dir.glob("*.png"):
            f.unlink()
        if temp_video.exists():
            temp_video.unlink()

        audio.close()

        print(f"Done: {output_path}")
        return output_path

    def _create_video_frames(
        self,
        frames_dir: Path,
        duration: float,
        script_data: dict,
        bg_style: str
    ):
        """Create all video frames with animated background and text"""

        total_frames = int(duration * self.fps)
        subtitle_lines = script_data.get("subtitle_lines", [])
        title = script_data.get("title", "")
        arabic_ayat = script_data.get("arabic_ayat", "")

        # Calculate timing
        frames_per_subtitle = total_frames // max(len(subtitle_lines), 1)

        # Font setup
        title_font = get_arabic_font(70)
        arabic_font = get_arabic_font(55)
        subtitle_font = get_arabic_font(45)

        # Generate stars for starfield
        np.random.seed(42)
        stars = self._generate_stars(100)

        print(f"Creating {total_frames} frames...")

        for frame_num in range(total_frames):
            # Create frame
            img = Image.new('RGB', (self.width, self.height))
            draw = ImageDraw.Draw(img)

            # Draw background
            self._draw_background(draw, frame_num, bg_style, stars)

            # Draw crescent moon
            self._draw_moon(draw, frame_num)

            # Draw title (first 5 seconds)
            if frame_num < self.fps * 5:
                self._draw_centered_text(
                    draw, title, title_font,
                    y=80, color=(255, 255, 255),
                    shadow=True
                )

            # Draw Arabic ayat (first 8 seconds)
            if frame_num < self.fps * 8 and arabic_ayat:
                alpha = min(255, frame_num * 10)  # Fade in
                self._draw_centered_text(
                    draw, arabic_ayat, arabic_font,
                    y=180, color=(255, 215, 0),
                    shadow=True
                )

            # Draw current subtitle
            current_subtitle_idx = min(
                frame_num // frames_per_subtitle,
                len(subtitle_lines) - 1
            )

            if current_subtitle_idx >= 0 and current_subtitle_idx < len(subtitle_lines):
                subtitle = subtitle_lines[current_subtitle_idx]
                self._draw_subtitle(draw, subtitle, subtitle_font, frame_num, frames_per_subtitle)

            # Save frame
            img.save(frames_dir / f"frame_{frame_num:04d}.png")

            if frame_num % 100 == 0:
                print(f"  Frame {frame_num}/{total_frames}")

    def _generate_stars(self, count: int) -> list:
        """Generate random stars"""
        stars = []
        for _ in range(count):
            stars.append({
                'x': np.random.randint(0, self.width),
                'y': np.random.randint(0, self.height),
                'size': np.random.randint(1, 4),
                'speed': np.random.uniform(0.2, 1.0),
                'brightness': np.random.randint(150, 255)
            })
        return stars

    def _draw_background(self, draw, frame_num, style, stars):
        """Draw animated background"""

        # Gradient
        for y in range(self.height):
            r = int(8 + 12 * y / self.height)
            g = int(12 + 20 * y / self.height)
            b = int(28 + 35 * y / self.height)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        # Stars
        for star in stars:
            brightness = star['brightness'] + int(20 * math.sin(frame_num * 0.08 + star['x'] * 0.01))
            brightness = max(100, min(255, brightness))

            x = star['x']
            y = (star['y'] + frame_num * star['speed']) % self.height

            color = (brightness, brightness, int(brightness * 0.95))
            s = star['size']

            if s == 1:
                draw.point((int(x), int(y)), fill=color)
            else:
                draw.ellipse([x-s, y-s, x+s, y+s], fill=color)

    def _draw_moon(self, draw, frame_num):
        """Draw crescent moon"""
        moon_x = self.width - 150
        moon_y = 120

        # Subtle glow
        for i in range(3, 0, -1):
            alpha = 30 + i * 10
            draw.ellipse([moon_x-45-i*3, moon_y-45-i*3, moon_x+45+i*3, moon_y+45+i*3],
                        fill=(alpha, alpha, int(alpha*0.8)))

        # Moon
        draw.ellipse([moon_x-40, moon_y-40, moon_x+40, moon_y+40],
                    fill=(255, 250, 230))
        # Crescent shadow
        draw.ellipse([moon_x-15, moon_y-45, moon_x+60, moon_y+45],
                    fill=(15, 22, 45))

    def _draw_centered_text(self, draw, text, font, y, color, shadow=False):
        """Draw centered text (RTL supported)"""
        if not text:
            return

        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2

            if shadow:
                draw.text((x + 3, y + 3), text, fill=(0, 0, 0), font=font)

            draw.text((x, y), text, fill=color, font=font)
        except Exception as e:
            print(f"Text error: {e}")

    def _draw_subtitle(self, draw, text, font, frame_num, frames_per_subtitle):
        """Draw subtitle with animation"""
        if not text:
            return

        # Position at bottom
        y = self.height - 150

        # Fade effect within each subtitle duration
        local_frame = frame_num % frames_per_subtitle
        fade_frames = 10

        if local_frame < fade_frames:
            # Fade in
            alpha = int(255 * local_frame / fade_frames)
        elif local_frame > frames_per_subtitle - fade_frames:
            # Fade out
            alpha = int(255 * (frames_per_subtitle - local_frame) / fade_frames)
        else:
            alpha = 255

        # Draw text box background
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x = (self.width - text_width) // 2

            # Semi-transparent background
            padding = 20
            draw.rectangle(
                [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
                fill=(0, 0, 0, 150)
            )

            # Text shadow
            draw.text((x + 2, y + 2), text, fill=(0, 0, 0), font=font)

            # Main text
            draw.text((x, y), text, fill=(255, 255, 255), font=font)

        except Exception as e:
            # Fallback
            draw.text((100, y), text, fill=(255, 255, 255), font=font)


def create_thumbnail_urdu(
    title: str,
    arabic_text: str,
    output_path: Path,
) -> Path:
    """Create thumbnail with Urdu/Arabic text"""

    img = Image.new('RGB', (1920, 1080))
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(1080):
        r = int(15 + 25 * y / 1080)
        g = int(25 + 35 * y / 1080)
        b = int(45 + 40 * y / 1080)
        draw.line([(0, y), (1920, y)], fill=(r, g, b))

    # Moon
    draw.ellipse([1650, 80, 1800, 230], fill=(255, 250, 220))
    draw.ellipse([1700, 60, 1850, 210], fill=(25, 40, 70))

    # Fonts
    title_font = get_arabic_font(90)
    arabic_font = get_arabic_font(60)

    # Title
    try:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        x = (1920 - (bbox[2] - bbox[0])) // 2
        draw.text((x + 4, 404), title, fill=(0, 0, 0), font=title_font)
        draw.text((x, 400), title, fill=(255, 255, 255), font=title_font)
    except:
        pass

    # Arabic ayat
    if arabic_text:
        try:
            bbox = draw.textbbox((0, 0), arabic_text, font=arabic_font)
            x = (1920 - (bbox[2] - bbox[0])) // 2
            draw.text((x, 550), arabic_text, fill=(255, 215, 0), font=arabic_font)
        except:
            pass

    img.save(output_path)
    return output_path


if __name__ == "__main__":
    print("Urdu Video Creator loaded successfully")
    print(f"Arabic font available: {get_arabic_font(48)}")
