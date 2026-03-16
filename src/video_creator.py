"""
Video Creator Module
Creates professional videos with animated text overlays
"""
import os
import re
from pathlib import Path
from typing import List, Optional

from moviepy import (
    VideoFileClip,
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ColorClip,
)

from config import VIDEO_SETTINGS, OUTPUT_DIR


class VideoCreator:
    """Creates professional videos with text animations"""

    def __init__(self):
        self.width = VIDEO_SETTINGS["width"]
        self.height = VIDEO_SETTINGS["height"]
        self.fps = VIDEO_SETTINGS["fps"]

    def create_video_from_audio_and_images(
        self,
        audio_path: Path,
        image_paths: List[Path],
        output_path: Path = None,
        title: str = None,
        script_text: str = None,
    ) -> Path:
        """
        Create video with animated text overlays synced to audio
        """
        output_path = output_path or OUTPUT_DIR / "final_video.mp4"

        # Load audio
        audio = AudioFileClip(str(audio_path))
        total_duration = audio.duration

        # Create background video from images
        background = self._create_background_video(image_paths, total_duration)

        layers = [background]

        # Add title at the beginning
        if title:
            title_clip = self._create_animated_title(title, total_duration)
            if title_clip:
                layers.append(title_clip)

        # Add animated subtitles if script provided
        if script_text:
            subtitle_clips = self._create_subtitle_clips(script_text, total_duration)
            layers.extend(subtitle_clips)

        # Compose all layers
        video = CompositeVideoClip(layers, size=(self.width, self.height))

        # Add audio
        video = video.with_audio(audio)

        # Export with better quality
        video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            bitrate='5000k',
            threads=4,
            preset='medium',
            logger=None,
        )

        # Cleanup
        audio.close()
        video.close()

        return output_path

    def _create_background_video(
        self,
        image_paths: List[Path],
        total_duration: float
    ) -> CompositeVideoClip:
        """Create animated background from images with Ken Burns effect"""

        if not image_paths:
            # Dark gradient background
            return ColorClip(
                size=(self.width, self.height),
                color=(15, 20, 35),
                duration=total_duration
            )

        clips = []
        duration_per_image = total_duration / len(image_paths)

        for i, img_path in enumerate(image_paths):
            # Create image clip
            clip = ImageClip(str(img_path), duration=duration_per_image)

            # Resize to cover
            clip = clip.resized((self.width, self.height))

            # Set start time
            clip = clip.with_start(i * duration_per_image)

            clips.append(clip)

        return CompositeVideoClip(clips, size=(self.width, self.height))

    def _create_animated_title(
        self,
        title: str,
        total_duration: float
    ) -> Optional[TextClip]:
        """Create animated title that appears at the start"""
        try:
            # Title appears for first 5 seconds
            title_duration = min(5, total_duration)

            txt_clip = TextClip(
                text=title,
                font_size=65,
                color='white',
                font='/System/Library/Fonts/Helvetica.ttc',
                stroke_color='black',
                stroke_width=3,
                size=(self.width - 100, None),
                method='caption',
                text_align='center',
            )

            # Position at top
            txt_clip = txt_clip.with_position(('center', 80))
            txt_clip = txt_clip.with_duration(title_duration)

            return txt_clip

        except Exception as e:
            print(f"Could not create title: {e}")
            return None

    def _create_subtitle_clips(
        self,
        script_text: str,
        total_duration: float
    ) -> List[TextClip]:
        """Create animated subtitle clips synced with audio"""
        from src.voice_generator import get_spoken_lines

        # Get clean lines
        lines = get_spoken_lines(script_text)

        if not lines:
            return []

        # Calculate timing
        time_per_line = total_duration / len(lines)
        subtitle_clips = []

        for i, line in enumerate(lines):
            start_time = i * time_per_line

            try:
                # Create text clip
                txt = TextClip(
                    text=line[:120],  # Limit line length
                    font_size=42,
                    color='white',
                    font='/System/Library/Fonts/Helvetica.ttc',
                    stroke_color='black',
                    stroke_width=2,
                    size=(self.width - 150, None),
                    method='caption',
                    text_align='center',
                )

                # Position at bottom
                txt = txt.with_position(('center', self.height - 180))
                txt = txt.with_start(start_time)
                txt = txt.with_duration(time_per_line)

                subtitle_clips.append(txt)

            except Exception as e:
                print(f"Skipping line {i}: {e}")
                continue

        return subtitle_clips

    def create_simple_video(
        self,
        audio_path: Path,
        output_path: Path = None,
        title: str = None,
        script_text: str = None,
    ) -> Path:
        """
        Create video with gradient background and text animations
        """
        output_path = output_path or OUTPUT_DIR / "simple_video.mp4"

        # Load audio
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration

        # Create gradient background
        background = self._create_gradient_background(duration)

        layers = [background]

        # Add title
        if title:
            title_clip = self._create_animated_title(title, duration)
            if title_clip:
                layers.append(title_clip)

        # Add subtitles
        if script_text:
            subtitle_clips = self._create_subtitle_clips(script_text, duration)
            layers.extend(subtitle_clips)

        # Compose
        video = CompositeVideoClip(layers, size=(self.width, self.height))
        video = video.with_audio(audio)

        # Export
        video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            bitrate='5000k',
            threads=4,
            logger=None,
        )

        audio.close()
        video.close()

        return output_path

    def _create_gradient_background(self, duration: float) -> ImageClip:
        """Create a gradient background image"""
        try:
            from PIL import Image, ImageDraw

            # Create gradient
            img = Image.new('RGB', (self.width, self.height))
            draw = ImageDraw.Draw(img)

            # Dark blue gradient
            color1 = (10, 15, 35)
            color2 = (25, 40, 70)

            for y in range(self.height):
                r = int(color1[0] + (color2[0] - color1[0]) * y / self.height)
                g = int(color1[1] + (color2[1] - color1[1]) * y / self.height)
                b = int(color1[2] + (color2[2] - color1[2]) * y / self.height)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b))

            # Save temporarily
            temp_path = OUTPUT_DIR / "_temp_gradient.png"
            img.save(temp_path)

            # Create clip
            clip = ImageClip(str(temp_path), duration=duration)

            return clip

        except Exception:
            return ColorClip(
                size=(self.width, self.height),
                color=(15, 25, 45),
                duration=duration
            )


def create_thumbnail(
    title: str,
    output_path: Path,
    background_color: tuple = (20, 35, 60),
    text_color: str = "white",
) -> Path:
    """
    Create a professional thumbnail image
    """
    try:
        from PIL import Image, ImageDraw, ImageFont

        # Create gradient background
        img = Image.new('RGB', (1920, 1080))
        draw = ImageDraw.Draw(img)

        # Gradient
        color1 = background_color
        color2 = (color1[0] + 30, color1[1] + 30, color1[2] + 30)

        for y in range(1080):
            r = int(color1[0] + (color2[0] - color1[0]) * y / 1080)
            g = int(color1[1] + (color2[1] - color1[1]) * y / 1080)
            b = int(color1[2] + (color2[2] - color1[2]) * y / 1080)
            draw.line([(0, y), (1920, y)], fill=(r, g, b))

        # Add decorative elements
        # Moon/crescent shape
        draw.ellipse([1600, 80, 1800, 280], fill=(255, 215, 0, 128))
        draw.ellipse([1650, 60, 1850, 260], fill=color2)

        # Try to use a nice font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 90)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        except Exception:
            font = ImageFont.load_default()
            small_font = font

        # Calculate text position
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (1920 - text_width) // 2
        y = (1080 - text_height) // 2

        # Draw text with shadow
        draw.text((x + 4, y + 4), title, fill=(0, 0, 0), font=font)
        draw.text((x, y), title, fill=text_color, font=font)

        # Add "Islamic Stories" subtitle
        subtitle = "Islamic Stories"
        draw.text((100, 950), subtitle, fill=(200, 200, 200), font=small_font)

        img.save(output_path)
        return output_path

    except ImportError:
        print("Pillow not available for thumbnail creation")
        return None


if __name__ == "__main__":
    print("Video Creator module loaded successfully")
