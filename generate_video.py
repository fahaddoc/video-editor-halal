"""
Video Generation Module - Actually creates videos!
"""
import os
import sys
import math
import subprocess
import asyncio
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from config import OUTPUT_DIR, ASSETS_DIR

# Arabic-supporting fonts on macOS
ARABIC_FONTS = [
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/GeezaPro.ttc",
    "/System/Library/Fonts/Supplemental/Geeza Pro.ttf",
]

def get_font(size=48):
    """Get Arabic-supporting font"""
    for font_path in ARABIC_FONTS:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    return ImageFont.load_default()


def generate_video(
    script_urdu: str,
    title_urdu: str = "",
    arabic_text: str = "",
    captions: list = None,
    voice: str = "ur-PK-AsadNeural",
    voice_speed: str = "-5%",
    output_name: str = "output_video",
    progress_callback=None
):
    """
    Generate complete video with audio and captions
    """
    import edge_tts

    output_path = OUTPUT_DIR / f"{output_name}.mp4"
    audio_path = OUTPUT_DIR / f"{output_name}_audio.mp3"
    frames_dir = ASSETS_DIR / "render_frames"
    frames_dir.mkdir(exist_ok=True)

    # Clean previous frames
    for f in frames_dir.glob("*.png"):
        f.unlink()

    if progress_callback:
        progress_callback(5, "🎙️ Generating voice...")

    # Step 1: Generate audio
    async def gen_audio():
        communicate = edge_tts.Communicate(
            text=script_urdu,
            voice=voice,
            rate=voice_speed
        )
        await communicate.save(str(audio_path))

    asyncio.run(gen_audio())

    if progress_callback:
        progress_callback(20, "📏 Calculating duration...")

    # Get audio duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())

    if progress_callback:
        progress_callback(25, f"🎬 Creating {int(duration)}s video...")

    # Step 2: Generate frames
    fps = 24
    total_frames = int(duration * fps)
    width, height = 1920, 1080

    # Prepare captions
    if not captions:
        captions = [l.strip() for l in script_urdu.split('\n') if l.strip() and len(l.strip()) > 5]

    frames_per_caption = max(1, total_frames // len(captions)) if captions else total_frames

    # Generate stars
    np.random.seed(42)
    stars = []
    for _ in range(120):
        stars.append({
            'x': np.random.randint(0, width),
            'y': np.random.randint(0, height),
            'size': np.random.randint(1, 4),
            'speed': np.random.uniform(0.2, 0.8),
            'brightness': np.random.randint(150, 255)
        })

    # Fonts
    title_font = get_font(60)
    arabic_font = get_font(50)
    caption_font = get_font(44)

    for frame_num in range(total_frames):
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        # Background gradient
        for y in range(height):
            r = int(8 + 15 * y / height)
            g = int(12 + 20 * y / height)
            b = int(25 + 40 * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Stars
        for star in stars:
            brightness = star['brightness'] + int(20 * math.sin(frame_num * 0.06 + star['x'] * 0.01))
            brightness = max(80, min(255, brightness))
            x = star['x']
            y = (star['y'] + frame_num * star['speed']) % height
            color = (brightness, brightness, int(brightness * 0.9))
            s = star['size']
            if s == 1:
                draw.point((int(x), int(y)), fill=color)
            else:
                draw.ellipse([x-s, y-s, x+s, y+s], fill=color)

        # Crescent moon
        moon_x, moon_y = width - 140, 100
        draw.ellipse([moon_x-40, moon_y-40, moon_x+40, moon_y+40], fill=(255, 250, 220))
        draw.ellipse([moon_x-15, moon_y-45, moon_x+55, moon_y+45], fill=(15, 22, 45))

        # Title (first 6 seconds)
        if frame_num < fps * 6 and title_urdu:
            try:
                bbox = draw.textbbox((0, 0), title_urdu, font=title_font)
                tw = bbox[2] - bbox[0]
                x = (width - tw) // 2
                draw.text((x+2, 82), title_urdu, fill=(0, 0, 0), font=title_font)
                draw.text((x, 80), title_urdu, fill=(255, 255, 255), font=title_font)
            except:
                pass

        # Arabic text (first 8 seconds)
        if frame_num < fps * 8 and arabic_text:
            try:
                bbox = draw.textbbox((0, 0), arabic_text, font=arabic_font)
                tw = bbox[2] - bbox[0]
                x = (width - tw) // 2
                draw.text((x+2, 172), arabic_text, fill=(0, 0, 0), font=arabic_font)
                draw.text((x, 170), arabic_text, fill=(255, 215, 0), font=arabic_font)
            except:
                pass

        # Caption
        if captions:
            caption_idx = min(frame_num // frames_per_caption, len(captions) - 1)
            caption = captions[caption_idx]

            try:
                bbox = draw.textbbox((0, 0), caption, font=caption_font)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                x = (width - tw) // 2
                y = height - 180

                # Background box
                padding = 20
                draw.rectangle(
                    [x - padding, y - padding, x + tw + padding, y + th + padding],
                    fill=(0, 0, 0, 200)
                )

                # Text
                draw.text((x+2, y+2), caption, fill=(0, 0, 0), font=caption_font)
                draw.text((x, y), caption, fill=(255, 255, 255), font=caption_font)
            except:
                pass

        # Save frame
        img.save(frames_dir / f"frame_{frame_num:05d}.png")

        # Progress update
        if frame_num % 50 == 0 and progress_callback:
            pct = 25 + int(50 * frame_num / total_frames)
            progress_callback(pct, f"🎨 Rendering frame {frame_num}/{total_frames}")

    if progress_callback:
        progress_callback(80, "🎬 Compiling video...")

    # Step 3: Compile frames to video
    temp_video = OUTPUT_DIR / "temp_render.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "20",
        str(temp_video)
    ]
    subprocess.run(cmd, capture_output=True)

    if progress_callback:
        progress_callback(90, "🔊 Adding audio...")

    # Step 4: Add audio
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

    if progress_callback:
        progress_callback(95, "🧹 Cleaning up...")

    # Cleanup
    for f in frames_dir.glob("*.png"):
        f.unlink()
    if temp_video.exists():
        temp_video.unlink()

    if progress_callback:
        progress_callback(100, "✅ Complete!")

    return output_path, audio_path


if __name__ == "__main__":
    # Test
    test_script = """
رسول اللہ صلی اللہ علیہ وسلم نے فرمایا:
اپنے بھائی کے سامنے مسکرانا صدقہ ہے۔
یہ حدیث جامع ترمذی میں ہے۔
"""

    def progress(pct, msg):
        print(f"[{pct}%] {msg}")

    video, audio = generate_video(
        script_urdu=test_script,
        title_urdu="مسکرانا صدقہ ہے",
        arabic_text="تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ",
        progress_callback=progress
    )

    print(f"\nVideo: {video}")
    print(f"Audio: {audio}")
