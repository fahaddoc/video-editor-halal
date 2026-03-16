"""
Video Creator Module
Combines audio, images, and text into final video using MoviePy
"""
import os
from pathlib import Path
from typing import List, Optional
from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ColorClip,
)
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
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

        Args:
            audio_path: Path to voiceover audio
            image_paths: List of background images/videos
            output_path: Where to save final video
            title: Optional title to overlay

        Returns:
            Path to created video
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
                # It's a video
                clip = VideoFileClip(str(img_path))
                clip = clip.loop(duration=duration_per_image)
            else:
                # It's an image
                clip = ImageClip(str(img_path), duration=duration_per_image)

            # Resize to fit
            clip = clip.resize((self.width, self.height))

            # Add fade effects
            clip = fadein(clip, 0.5)
            clip = fadeout(clip, 0.5)

            clips.append(clip)

        # Concatenate all clips
        if clips:
            video = concatenate_videoclips(clips, method="compose")
        else:
            # Fallback: black background
            video = ColorClip(
                size=(self.width, self.height),
                color=(20, 20, 30),
                duration=total_duration
            )

        # Add title if provided
        if title:
            title_clip = self._create_title_clip(title, duration=4)
            video = CompositeVideoClip([video, title_clip])

        # Add audio
        video = video.set_audio(audio)

        # Export
        video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            preset='medium',
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
        title: str = None,
        subtitle_text: str = None,
    ) -> Path:
        """
        Create a simple video with solid background

        Args:
            audio_path: Path to voiceover
            output_path: Where to save
            background_color: RGB tuple for background
            title: Title text
            subtitle_text: Scrolling subtitle text

        Returns:
            Path to video
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

        layers = [background]

        # Add title
        if title:
            title_clip = self._create_title_clip(title, duration=duration)
            layers.append(title_clip)

        # Compose
        video = CompositeVideoClip(layers)
        video = video.set_audio(audio)

        # Export
        video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            threads=4,
        )

        audio.close()
        video.close()

        return output_path

    def _create_title_clip(
        self,
        title: str,
        duration: float,
        fontsize: int = 70,
        color: str = 'white',
        position: tuple = ('center', 100),
    ) -> TextClip:
        """Create a title text clip"""
        try:
            txt_clip = TextClip(
                title,
                fontsize=fontsize,
                color=color,
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=2,
            )
            txt_clip = txt_clip.set_position(position)
            txt_clip = txt_clip.set_duration(duration)
            txt_clip = fadein(txt_clip, 1)
            return txt_clip
        except Exception as e:
            print(f"Could not create title clip: {e}")
            # Return empty clip on error
            return ColorClip(
                size=(1, 1),
                color=(0, 0, 0, 0),
                duration=duration
            ).set_position(position)

    def create_video_with_text_animation(
        self,
        audio_path: Path,
        script_lines: List[str],
        output_path: Path = None,
        background_color: tuple = (15, 20, 30),
    ) -> Path:
        """
        Create video with animated text (like subtitles)

        Args:
            audio_path: Path to audio
            script_lines: Lines of script to animate
            output_path: Where to save
            background_color: Background RGB

        Returns:
            Path to video
        """
        output_path = output_path or OUTPUT_DIR / "text_video.mp4"

        # Load audio
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration

        # Create background
        background = ColorClip(
            size=(self.width, self.height),
            color=background_color,
            duration=duration
        )

        # Calculate timing for each line
        lines = [l for l in script_lines if l.strip()]
        time_per_line = duration / max(len(lines), 1)

        text_clips = []
        for i, line in enumerate(lines):
            start_time = i * time_per_line
            line_duration = time_per_line

            try:
                txt = TextClip(
                    line[:100],  # Limit line length
                    fontsize=50,
                    color='white',
                    font='Arial',
                    size=(self.width - 200, None),
                    method='caption',
                )
                txt = txt.set_position('center')
                txt = txt.set_start(start_time)
                txt = txt.set_duration(line_duration)
                txt = fadein(txt, 0.3)
                txt = fadeout(txt, 0.3)
                text_clips.append(txt)
            except Exception:
                continue

        # Compose
        video = CompositeVideoClip([background] + text_clips)
        video = video.set_audio(audio)

        # Export
        video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
        )

        audio.close()
        video.close()
        for clip in text_clips:
            try:
                clip.close()
            except Exception:
                pass

        return output_path


def create_thumbnail(
    title: str,
    output_path: Path,
    background_color: tuple = (30, 40, 60),
    text_color: str = "white",
) -> Path:
    """
    Create a simple thumbnail image

    Args:
        title: Text for thumbnail
        output_path: Where to save
        background_color: RGB background
        text_color: Text color

    Returns:
        Path to thumbnail
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
    # Test
    print("Video Creator module loaded successfully")
