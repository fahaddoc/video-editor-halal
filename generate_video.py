"""
Video Generation Module - Creates professional Islamic videos
With proper Arabic/Urdu voice switching and caption sync
"""
import os
import sys
import math
import subprocess
import asyncio
import nest_asyncio
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display

# Fix asyncio for Streamlit compatibility
nest_asyncio.apply()

sys.path.insert(0, str(Path(__file__).parent))
from config import OUTPUT_DIR, ASSETS_DIR

# Arabic-supporting fonts on macOS
ARABIC_FONTS = [
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/GeezaPro.ttc",
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


def reshape_text(text):
    """Reshape Arabic/Urdu text for proper RTL rendering"""
    if not text:
        return text
    try:
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        return bidi_text
    except:
        return text


def is_arabic_text(text):
    """Check if text is Arabic (has harakat/diacritics)"""
    # Arabic harakat (tashkeel) - indicates Quranic/formal Arabic
    harakat_pattern = r'[\u064B-\u065F\u0670]'
    return bool(re.search(harakat_pattern, text))


def get_audio_duration(audio_path):
    """Get duration of audio file in seconds"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


async def generate_line_audio(text, voice, rate, pitch, output_path):
    """Generate audio for a single line"""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(str(output_path))


async def generate_synced_audio(
    lines,
    urdu_voice,
    arabic_voice,
    urdu_rate,
    urdu_pitch,
    arabic_rate,
    arabic_pitch,
    output_dir
):
    """Generate audio with proper Arabic/Urdu voice switching and timing info"""
    import edge_tts

    audio_segments = []
    timing_info = []
    current_time = 0.0

    for i, line in enumerate(lines):
        if not line.strip():
            continue

        temp_audio = output_dir / f"temp_line_{i}.mp3"

        # Detect if line is Arabic (has harakat)
        if is_arabic_text(line):
            voice = arabic_voice
            rate = arabic_rate
            pitch = arabic_pitch
            lang = 'arabic'
        else:
            voice = urdu_voice
            rate = urdu_rate
            pitch = urdu_pitch
            lang = 'urdu'

        # Generate audio for this line
        await generate_line_audio(line, voice, rate, pitch, temp_audio)

        # Get duration
        duration = get_audio_duration(temp_audio)

        # Store timing info
        timing_info.append({
            'text': line,
            'lang': lang,
            'start': current_time,
            'duration': duration,
            'end': current_time + duration
        })

        audio_segments.append(temp_audio)
        current_time += duration + 0.3  # Small gap between lines

    return audio_segments, timing_info


def concatenate_audio(audio_files, output_path, gap=0.3):
    """Concatenate audio files with small gaps"""
    temp_dir = output_path.parent

    # Create silence file
    silence_file = temp_dir / "gap.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=mono",
        "-t", str(gap), "-q:a", "9",
        str(silence_file)
    ], capture_output=True)

    # Create concat file
    concat_file = temp_dir / "concat_list.txt"
    with open(concat_file, 'w') as f:
        for i, audio in enumerate(audio_files):
            f.write(f"file '{audio}'\n")
            if i < len(audio_files) - 1:
                f.write(f"file '{silence_file}'\n")

    # Concatenate
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(output_path)
    ], capture_output=True)

    # Cleanup
    for f in audio_files:
        if f.exists():
            f.unlink()
    if silence_file.exists():
        silence_file.unlink()
    if concat_file.exists():
        concat_file.unlink()


def generate_video(
    script_urdu: str,
    title_urdu: str = "",
    arabic_text: str = "",
    captions: list = None,
    voice: str = "ur-PK-AsadNeural",
    arabic_voice: str = "ar-EG-ShakirNeural",
    voice_speed: str = "-8%",
    urdu_pitch: str = "-18Hz",
    arabic_pitch: str = "-5Hz",
    include_arabic_recitation: bool = True,
    output_name: str = "output_video",
    progress_callback=None
):
    """Generate video with proper Arabic/Urdu sync"""
    import edge_tts

    output_path = OUTPUT_DIR / f"{output_name}.mp4"
    audio_path = OUTPUT_DIR / f"{output_name}_audio.mp3"
    frames_dir = ASSETS_DIR / "render_frames"
    frames_dir.mkdir(exist_ok=True)

    # Clean previous frames
    for f in frames_dir.glob("*.png"):
        f.unlink()

    if progress_callback:
        progress_callback(5, "🎙️ Generating voice with sync...")

    # Prepare lines for audio generation
    lines = [l.strip() for l in script_urdu.split('\n') if l.strip()]

    # If arabic_text is provided and include_arabic_recitation is True, add it at start
    if include_arabic_recitation and arabic_text and arabic_text.strip():
        lines = [arabic_text.strip()] + lines

    # Generate audio with timing info
    async def gen_audio():
        segments, timing = await generate_synced_audio(
            lines=lines,
            urdu_voice=voice,
            arabic_voice=arabic_voice,
            urdu_rate=voice_speed,
            urdu_pitch=urdu_pitch,
            arabic_rate="-15%",  # Slower for Arabic recitation
            arabic_pitch=arabic_pitch,
            output_dir=OUTPUT_DIR
        )
        return segments, timing

    audio_segments, timing_info = asyncio.run(gen_audio())

    if progress_callback:
        progress_callback(15, "🔗 Combining audio...")

    # Concatenate all audio
    concatenate_audio(audio_segments, audio_path, gap=0.3)

    if progress_callback:
        progress_callback(20, "📏 Calculating duration...")

    # Get total duration
    duration = get_audio_duration(audio_path)

    if progress_callback:
        progress_callback(25, f"🎬 Creating {int(duration)}s video...")

    # Step 2: Generate frames
    fps = 24
    total_frames = int(duration * fps)
    width, height = 1920, 1080

    # Reshape text for display
    title_display = reshape_text(title_urdu) if title_urdu else ""
    arabic_display = reshape_text(arabic_text) if arabic_text else ""

    # Prepare caption timing from audio sync info
    caption_timing = []
    for info in timing_info:
        caption_timing.append({
            'text': reshape_text(info['text']),
            'original': info['text'],
            'lang': info['lang'],
            'start_frame': int(info['start'] * fps),
            'end_frame': int(info['end'] * fps),
        })

    # Background schemes
    bg_change_frames = fps * 6
    bg_schemes = [
        {'r1': 5, 'g1': 8, 'b1': 25, 'r2': 15, 'g2': 25, 'b2': 60},
        {'r1': 15, 'g1': 5, 'b1': 25, 'r2': 40, 'g2': 15, 'b2': 50},
        {'r1': 5, 'g1': 15, 'b1': 20, 'r2': 10, 'g2': 35, 'b2': 45},
        {'r1': 3, 'g1': 3, 'b1': 15, 'r2': 10, 'g2': 10, 'b2': 35},
    ]

    # Generate stars and particles
    np.random.seed(42)
    stars = [{'x': np.random.randint(0, width), 'y': np.random.randint(0, height),
              'size': np.random.randint(1, 4), 'speed': np.random.uniform(0.1, 0.5),
              'brightness': np.random.randint(150, 255), 'twinkle': np.random.uniform(0.03, 0.1)}
             for _ in range(180)]

    particles = [{'x': np.random.randint(0, width), 'y': np.random.randint(0, height),
                  'size': np.random.randint(2, 5), 'speed_y': np.random.uniform(-0.4, -0.1),
                  'alpha': np.random.randint(30, 70)}
                 for _ in range(35)]

    # Fonts
    title_font = get_font(72)
    arabic_font = get_font(58)
    caption_font = get_font(50)

    for frame_num in range(total_frames):
        img = Image.new('RGBA', (width, height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)

        # Background with smooth transitions
        bg_idx = (frame_num // bg_change_frames) % len(bg_schemes)
        bg = bg_schemes[bg_idx]

        for y in range(height):
            py = y / height
            r = int(bg['r1'] + (bg['r2'] - bg['r1']) * py)
            g = int(bg['g1'] + (bg['g2'] - bg['g1']) * py)
            b = int(bg['b1'] + (bg['b2'] - bg['b1']) * py)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        # Stars
        for star in stars:
            twinkle = math.sin(frame_num * star['twinkle'] + star['x'] * 0.01)
            brightness = int(star['brightness'] + 50 * twinkle)
            brightness = max(60, min(255, brightness))
            x, y = star['x'], (star['y'] + frame_num * star['speed']) % height
            s = star['size']
            draw.ellipse([x-s, y-s, x+s, y+s], fill=(brightness, brightness, int(brightness*0.9), 255))

        # Particles
        for p in particles:
            px = p['x']
            py = (p['y'] + frame_num * p['speed_y']) % height
            pa = p['alpha'] + int(15 * math.sin(frame_num * 0.05))
            draw.ellipse([px-p['size'], py-p['size'], px+p['size'], py+p['size']],
                        fill=(255, 215, 0, max(20, min(80, pa))))

        # Moon
        moon_x, moon_y = width - 150, 110
        glow = 1 + 0.08 * math.sin(frame_num * 0.025)
        for gs in range(int(60*glow), int(40*glow), -4):
            ga = int(20 * (60 - gs) / 20)
            draw.ellipse([moon_x-gs, moon_y-gs, moon_x+gs, moon_y+gs], fill=(255, 250, 200, ga))
        draw.ellipse([moon_x-42, moon_y-42, moon_x+42, moon_y+42], fill=(255, 252, 235, 255))
        draw.ellipse([moon_x-8, moon_y-50, moon_x+55, moon_y+50], fill=(bg['r1'], bg['g1'], bg['b1'], 255))

        # Title (first 5 seconds)
        if frame_num < fps * 5 and title_display:
            fade = min(255, int(255 * frame_num / (fps * 1))) if frame_num < fps else 255
            try:
                bbox = draw.textbbox((0, 0), title_display, font=title_font)
                tw = bbox[2] - bbox[0]
                x, y = (width - tw) // 2, 80
                draw.text((x+3, y+3), title_display, fill=(0, 0, 0, 180), font=title_font)
                draw.text((x, y), title_display, fill=(255, 255, 255, fade), font=title_font)
            except:
                pass

        # Find current caption based on timing
        current_caption = None
        for cap in caption_timing:
            if cap['start_frame'] <= frame_num < cap['end_frame']:
                current_caption = cap
                break

        if current_caption:
            text = current_caption['text']
            is_arabic = current_caption['lang'] == 'arabic'

            # Calculate fade
            frames_in = frame_num - current_caption['start_frame']
            frames_total = current_caption['end_frame'] - current_caption['start_frame']

            if frames_in < 6:
                alpha = int(255 * frames_in / 6)
            elif frames_in > frames_total - 6:
                alpha = int(255 * (frames_total - frames_in) / 6)
            else:
                alpha = 255

            try:
                font = arabic_font if is_arabic else caption_font
                bbox = draw.textbbox((0, 0), text, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

                if is_arabic:
                    # Arabic text - special styling at top area
                    x = (width - tw) // 2
                    y = 180

                    # Golden glow for Arabic
                    for offset in range(4, 0, -1):
                        draw.text((x, y), text, fill=(255, 200, 0, 30), font=font)

                    # Border box
                    padding = 25
                    draw.rounded_rectangle(
                        [x-padding, y-padding, x+tw+padding, y+th+padding],
                        radius=12, outline=(255, 215, 0, 150), width=2
                    )

                    draw.text((x+2, y+2), text, fill=(0, 0, 0, alpha), font=font)
                    draw.text((x, y), text, fill=(255, 215, 0, alpha), font=font)
                else:
                    # Urdu text - center of screen
                    x = (width - tw) // 2
                    y = (height - th) // 2 + 80

                    # Background box
                    padding = 30
                    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
                    ov_draw = ImageDraw.Draw(overlay)
                    ov_draw.rounded_rectangle(
                        [x-padding, y-padding, x+tw+padding, y+th+padding],
                        radius=15, fill=(0, 0, 0, 160)
                    )
                    img = Image.alpha_composite(img, overlay)
                    draw = ImageDraw.Draw(img)

                    # Border
                    draw.rounded_rectangle(
                        [x-padding-2, y-padding-2, x+tw+padding+2, y+th+padding+2],
                        radius=17, outline=(255, 215, 0, 80), width=2
                    )

                    draw.text((x+2, y+2), text, fill=(0, 0, 0, alpha), font=caption_font)
                    draw.text((x, y), text, fill=(255, 255, 255, alpha), font=caption_font)
            except:
                pass

        # Save frame
        img_rgb = Image.new('RGB', img.size, (0, 0, 0))
        img_rgb.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
        img_rgb.save(frames_dir / f"frame_{frame_num:05d}.png")

        if frame_num % 50 == 0 and progress_callback:
            pct = 25 + int(50 * frame_num / total_frames)
            progress_callback(pct, f"🎨 Rendering frame {frame_num}/{total_frames}")

    if progress_callback:
        progress_callback(80, "🎬 Compiling video...")

    # Compile video
    temp_video = OUTPUT_DIR / "temp_render.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        str(temp_video)
    ], capture_output=True)

    if progress_callback:
        progress_callback(90, "🔊 Adding audio...")

    # Add audio
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(temp_video), "-i", str(audio_path),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(output_path)
    ], capture_output=True)

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
    test_script = """رسول اللہ صلی اللہ علیہ وسلم نے فرمایا۔
تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ
اپنے بھائی کے سامنے مسکرانا صدقہ ہے۔
یہ حدیث جامع ترمذی میں ہے۔
مسکرانا بھی صدقہ ہے۔
سبسکرائب کریں۔"""

    def progress(pct, msg):
        print(f"[{pct}%] {msg}")

    video, audio = generate_video(
        script_urdu=test_script,
        title_urdu="مسکرانے کی طاقت",
        arabic_text="تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ",
        include_arabic_recitation=True,
        progress_callback=progress
    )
    print(f"\nVideo: {video}")
