"""
Video Creator Module
Combines audio, images, and text into final video using MoviePy
"""
import os
from pathlib import Path
from typing import List, Optional

# MoviePy 2.x imports
from moviepy import (
    VideoFileClip,
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ColorClip,
)
from moviepy.video.fx import CrossFadeIn, CrossFadeOut

from config import VIDEO_SETTINGS, OUTPUT_DIR


class VideoCreator:
    """Creates videos from audio, images, and text"""

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
    ) -> Path:
        """
        Create video from audio and images
        """
        output_path = output_path or OUTPUT_DIR / "final_video.mp4"

        # Load audio
        audio = AudioFileClip(str(audio_path))
        total_duration = audio.duration

        # Create video clips from images
        clips = []
        duration_per_image = total_duration / max(len(image_paths), 1)

        for img_path in image_paths:
            if str(img_path).endswith(('.mp4', '.mov', '.avi')):
                clip = VideoFileClip(str(img_path))
            else:
                clip = ImageClip(str(img_path), duration=duration_per_image)

            # Resize to fit
            clip = clip.resized((self.width, self.height))

            # Set duration for images
            if not str(img_path).endswith(('.mp4', '.mov', '.avi')):
                clip = clip.with_duration(duration_per_image)

            clips.append(clip)

        # Concatenate all clips
        if clips:
            video = concatenate_videoclips(clips, method="compose")
        else:
            video = ColorClip(
                size=(self.width, self.height),
                color=(20, 20, 30),
                duration=total_duration
            )

        # Add audio
        video = video.with_audio(audio)

        # Export
        video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            preset='medium',
            logger=None,
        )

        # Cleanup
        audio.close()
        video.close()
        for clip in clips:
            clip.close()

        return output_path

    def create_simple_video(
        self,
        audio_path: Path,
        output_path: Path = None,
        background_color: tuple = (20, 25, 35),
    ) -> Path:
        """
        Create a simple video with solid background
        """
        output_path = output_path or OUTPUT_DIR / "simple_video.mp4"

        # Load audio
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration

        # Create background
        background = ColorClip(
            size=(self.width, self.height),
            color=background_color,
            duration=duration
        )

        # Compose
        video = background.with_audio(audio)

        # Export
        video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            logger=None,
        )

        audio.close()
        video.close()

        return output_path


def create_thumbnail(
    title: str,
    output_path: Path,
    background_color: tuple = (30, 40, 60),
    text_color: str = "white",
) -> Path:
    """
    Create a simple thumbnail image
    """
    try:
        from PIL import Image, ImageDraw, ImageFont

        # Create image
        img = Image.new('RGB', (1920, 1080), background_color)
        draw = ImageDraw.Draw(img)

        # Try to use a nice font, fallback to default
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        except Exception:
            font = ImageFont.load_default()

        # Calculate text position
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (1920 - text_width) // 2
        y = (1080 - text_height) // 2

        # Draw text with shadow
        draw.text((x + 3, y + 3), title, fill="black", font=font)
        draw.text((x, y), title, fill=text_color, font=font)

        img.save(output_path)
        return output_path

    except ImportError:
        print("Pillow not available for thumbnail creation")
        return None


if __name__ == "__main__":
    print("Video Creator module loaded successfully")
