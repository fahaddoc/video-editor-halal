"""
Video Generation Module - Creates professional Islamic videos
With proper Arabic/Urdu voice switching, caption sync, and text effects
"""
import os
import sys
import math
import subprocess
import asyncio
import nest_asyncio
import re
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display

# Fix asyncio for Streamlit compatibility
nest_asyncio.apply()

sys.path.insert(0, str(Path(__file__).parent))
from config import OUTPUT_DIR, ASSETS_DIR

# Import simple caption renderer
from src.caption_renderer import draw_caption, draw_arabic_caption

# Import dynamic backgrounds
from src.animated_backgrounds import (
    detect_theme, create_dynamic_theme_frame,
    generate_stars_particles, THEME_COLORS
)

# Import content categories and animated scenery
from src.content_categories import get_category, CONTENT_CATEGORIES
from src.animated_scenery import AnimatedScenery, HorrorScenery, KidsScenery

# Import caption visuals for per-caption images
from src.caption_visuals import get_caption_visuals

# Text effect options (for future use)
TEXT_EFFECTS = ["none", "fade", "karaoke", "typewriter"]

# Background modes
BG_MODES = ["static", "animated", "dynamic"]  # dynamic = keyword-based theme changes

# Arabic-supporting fonts - Amiri is best for harakat (zer zabar)
ASSETS_FONTS_DIR = Path(__file__).parent / "assets"

ARABIC_FONTS = [
    str(ASSETS_FONTS_DIR / "Amiri-Regular.ttf"),  # Best for Arabic with harakat
    str(ASSETS_FONTS_DIR / "Amiri-Bold.ttf"),
    "/System/Library/Fonts/GeezaPro.ttc",
    "/System/Library/Fonts/Supplemental/Al Nile.ttc",
    "/System/Library/Fonts/SFArabic.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]

# Cache for loaded fonts
_font_cache = {}


def get_font(size=48, bold=False):
    """Get Arabic-supporting font with harakat support"""
    cache_key = (size, bold)
    if cache_key in _font_cache:
        return _font_cache[cache_key]

    # Try Amiri Bold first if bold requested
    if bold:
        bold_path = str(ASSETS_FONTS_DIR / "Amiri-Bold.ttf")
        if os.path.exists(bold_path):
            try:
                font = ImageFont.truetype(bold_path, size)
                _font_cache[cache_key] = font
                return font
            except:
                pass

    # Try each font in order
    for font_path in ARABIC_FONTS:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, size)
                _font_cache[cache_key] = font
                return font
            except:
                continue

    return ImageFont.load_default()


def reshape_text(text):
    """Reshape Arabic/Urdu text for proper RTL rendering - preserves harakat"""
    if not text:
        return text
    try:
        # Configure reshaper to preserve harakat (zer, zabar, pesh, etc.)
        configuration = {
            'delete_harakat': False,
            'support_ligatures': True,
        }
        reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)
        reshaped = reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        return bidi_text
    except:
        return text


def is_arabic_text(text):
    """Check if text is Arabic (has harakat/diacritics)"""
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


def make_natural_text(text):
    """
    Process text to sound more natural with pauses and emphasis.
    Adds natural breathing pauses at punctuation marks.
    """
    if not text:
        return text

    # Add pauses after common punctuation for natural rhythm
    natural_text = text

    # Longer pause after full stop/period
    natural_text = natural_text.replace('۔', '۔...')  # Urdu full stop
    natural_text = natural_text.replace('।', '।...')  # Hindi full stop
    natural_text = natural_text.replace('.', '....')  # English period

    # Medium pause after question/exclamation
    natural_text = natural_text.replace('؟', '؟..')   # Urdu question
    natural_text = natural_text.replace('?', '?..')   # English question
    natural_text = natural_text.replace('!', '!..')   # Exclamation

    # Short pause after comma
    natural_text = natural_text.replace('،', '،.')    # Urdu comma
    natural_text = natural_text.replace(',', ',.')    # English comma

    # Pause after colon
    natural_text = natural_text.replace(':', ':.')

    # Add slight pause before important Islamic phrases
    islamic_phrases = [
        'صلی اللہ علیہ وسلم',
        'رضی اللہ عنہ',
        'سبحان اللہ',
        'الحمد للہ',
        'اللہ اکبر',
        'ان شاء اللہ',
        'ما شاء اللہ',
    ]
    for phrase in islamic_phrases:
        if phrase in natural_text:
            natural_text = natural_text.replace(phrase, f'... {phrase}')

    return natural_text


async def generate_line_audio(text, voice, rate, pitch, output_path, natural=True):
    """Generate audio for a single line with natural speech processing"""
    import edge_tts

    # Make text sound more natural
    processed_text = make_natural_text(text) if natural else text

    communicate = edge_tts.Communicate(processed_text, voice, rate=rate, pitch=pitch)
    await communicate.save(str(output_path))


def is_subscribe_line(text):
    """Check if line is a subscribe/CTA line that should be in English"""
    subscribe_keywords = [
        'سبسکرائب', 'subscribe', 'سبسکرائب کریں', 'لائک', 'like',
        'شیئر', 'share', 'بیل آئیکن', 'bell icon', 'کمنٹ', 'comment'
    ]
    text_lower = text.lower().strip()
    return any(keyword in text_lower for keyword in subscribe_keywords)


async def generate_synced_audio(
    lines,
    urdu_voice,
    arabic_voice,
    urdu_rate,
    urdu_pitch,
    arabic_rate,
    arabic_pitch,
    output_dir,
    first_line_is_arabic=False,  # Flag to indicate first line is Arabic hadith/ayat
    english_voice="en-US-GuyNeural"  # English voice for subscribe CTA
):
    """Generate audio with proper Arabic/Urdu/English voice switching and timing info"""
    import edge_tts

    audio_segments = []
    timing_info = []
    current_time = 0.0
    line_index = 0  # Track actual line index (excluding empty lines)

    for i, line in enumerate(lines):
        if not line.strip():
            continue

        temp_audio = output_dir / f"temp_line_{i}.mp3"

        # Check line type for voice selection
        if first_line_is_arabic and line_index == 0:
            # First line is Arabic hadith/ayat
            voice = arabic_voice
            rate = arabic_rate
            pitch = arabic_pitch
            lang = 'arabic'
        elif is_subscribe_line(line):
            # Subscribe/CTA line - use English voice with English text
            voice = english_voice
            rate = "-5%"  # Normal speed for English
            pitch = "-2Hz"
            lang = 'english'
            # Replace Urdu subscribe text with generic English
            line = "Subscribe for more stories. Like and share!"
        else:
            # Regular Urdu line
            voice = urdu_voice
            rate = urdu_rate
            pitch = urdu_pitch
            lang = 'urdu'

        line_index += 1

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
        current_time += duration + 0.5  # Natural pause between lines (slightly longer)

    return audio_segments, timing_info


def generate_audio_google(
    lines,
    urdu_voice,
    arabic_voice,
    speaking_rate,
    pitch,
    output_dir,
    progress_callback=None
):
    """Generate audio using Google Cloud TTS"""
    try:
        from src.google_tts import synthesize_speech_google, GOOGLE_VOICES, is_google_tts_ready
    except ImportError:
        raise Exception("Google TTS module not available")

    ready, msg = is_google_tts_ready()
    if not ready:
        raise Exception(f"Google TTS not ready: {msg}")

    audio_segments = []
    timing_info = []
    current_time = 0.0

    for i, line in enumerate(lines):
        if not line.strip():
            continue

        temp_audio = output_dir / f"temp_line_{i}.mp3"

        # Detect if line is Arabic
        if is_arabic_text(line):
            voice_id = arabic_voice if arabic_voice.startswith("google_") else "google_arabic_male"
            lang = 'arabic'
        else:
            voice_id = urdu_voice if urdu_voice.startswith("google_") else "google_urdu_male"
            lang = 'urdu'

        # Generate audio
        success = synthesize_speech_google(
            text=line,
            output_path=temp_audio,
            voice_id=voice_id,
            speaking_rate=speaking_rate,
            pitch=pitch
        )

        if not success:
            raise Exception(f"Failed to generate audio for line {i}")

        # Get duration
        duration = get_audio_duration(temp_audio)

        timing_info.append({
            'text': line,
            'lang': lang,
            'start': current_time,
            'duration': duration,
            'end': current_time + duration
        })

        audio_segments.append(temp_audio)
        current_time += duration + 0.3

        if progress_callback and i % 3 == 0:
            pct = 5 + int(10 * i / len(lines))
            progress_callback(pct, f"Generating voice {i+1}/{len(lines)}...")

    return audio_segments, timing_info


def concatenate_audio(audio_files, output_path, gap=0.5):
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
    voice_speed = "-8%",
    urdu_pitch = "-18Hz",
    arabic_pitch: str = "-5Hz",
    include_arabic_recitation: bool = True,
    output_name: str = "output_video",
    text_effect: str = "fade",
    tts_provider: str = "edge",
    resolution: str = "1080p",  # "1080p", "720p", "tiktok"
    custom_audio_path: str = None,  # User uploaded audio
    bg_mode: str = "scenery",  # "static", "animated", "dynamic", "scenery" (category-based)
    content_category: str = "halal",  # Content category for scenery
    background_audio: str = None,  # Background ASMR/ambient sound (e.g., "wind", "rain", "fire")
    background_volume: float = 0.3,  # Background audio volume (0.0 to 1.0)
    caption_images: dict = None,  # Dict mapping caption index to image path
    auto_generate_images: bool = False,  # Auto-generate AI images for captions
    image_style: str = "cinematic",  # Style for AI image generation
    progress_callback=None
):
    """
    Generate video with proper Arabic/Urdu sync and text effects

    Args:
        resolution: Video resolution - "1080p" (1920x1080), "720p" (1280x720), "tiktok" (1080x1920)
        custom_audio_path: Optional path to user-uploaded audio file (skips TTS generation)
        bg_mode: Background mode - "static", "animated", "dynamic", or "scenery" (category-based)
        content_category: Content type - "halal", "horror", "kids", "mystery", etc.
        background_audio: Background ambient sound - "wind", "rain", "fire", "night" or path to audio file
        background_volume: Volume level for background audio (0.0 to 1.0)
        caption_images: Dict mapping caption index to image path for per-caption backgrounds
        auto_generate_images: If True, auto-generate AI images for each caption
        image_style: Style for AI generation - "cinematic", "dark", "anime", "realistic"
    """
    output_path = OUTPUT_DIR / f"{output_name}.mp4"
    audio_path = OUTPUT_DIR / f"{output_name}_audio.mp3"
    frames_dir = ASSETS_DIR / "render_frames"
    frames_dir.mkdir(exist_ok=True)

    # Clean previous frames
    for f in frames_dir.glob("*.png"):
        f.unlink()

    # Check if using custom uploaded audio
    if custom_audio_path and os.path.exists(custom_audio_path):
        if progress_callback:
            progress_callback(5, "Using uploaded audio...")

        # Copy custom audio to output path
        shutil.copy(custom_audio_path, audio_path)

        # For custom audio, we generate caption timing based on captions and audio duration
        duration_audio = get_audio_duration(audio_path)

        # Use provided captions or generate from script
        if captions:
            lines = captions
        else:
            lines = [l.strip() for l in script_urdu.split('\n') if l.strip()]

        # Distribute captions evenly across audio duration
        # All lines are treated as Urdu for custom audio (user provides their own narration)
        timing_info = []
        if lines:
            time_per_caption = duration_audio / len(lines)
            current_time = 0.0
            for i, line in enumerate(lines):
                timing_info.append({
                    'text': line,
                    'lang': 'urdu',  # All Urdu for custom audio
                    'start': current_time,
                    'duration': time_per_caption,
                    'end': current_time + time_per_caption
                })
                current_time += time_per_caption

        if progress_callback:
            progress_callback(15, "Audio ready...")
    else:
        if progress_callback:
            progress_callback(5, "Generating voice...")

        # Prepare lines for audio generation
        lines = [l.strip() for l in script_urdu.split('\n') if l.strip()]

        # If arabic_text is provided and include_arabic_recitation is True, add it at start
        if include_arabic_recitation and arabic_text and arabic_text.strip():
            lines = [arabic_text.strip()] + lines

        # Generate audio based on TTS provider
        if tts_provider == "google":
            # Use Google Cloud TTS
            audio_segments, timing_info = generate_audio_google(
                lines=lines,
                urdu_voice=voice,
                arabic_voice=arabic_voice,
                speaking_rate=voice_speed if isinstance(voice_speed, float) else 0.85,
                pitch=urdu_pitch if isinstance(urdu_pitch, float) else -2.0,
                output_dir=OUTPUT_DIR,
                progress_callback=progress_callback
            )
        else:
            # Use Edge TTS
            import edge_tts
            # Check if first line is Arabic (when arabic recitation is included)
            has_arabic_first = include_arabic_recitation and arabic_text and arabic_text.strip()

            async def gen_audio():
                segments, timing = await generate_synced_audio(
                    lines=lines,
                    urdu_voice=voice,
                    arabic_voice=arabic_voice,
                    urdu_rate=voice_speed if isinstance(voice_speed, str) else "-15%",
                    urdu_pitch=urdu_pitch if isinstance(urdu_pitch, str) else "-10Hz",
                    arabic_rate="-15%",
                    arabic_pitch=arabic_pitch if isinstance(arabic_pitch, str) else "-5Hz",
                    output_dir=OUTPUT_DIR,
                    first_line_is_arabic=has_arabic_first  # Only first line is Arabic
                )
                return segments, timing

            audio_segments, timing_info = asyncio.run(gen_audio())

        if progress_callback:
            progress_callback(15, "Combining audio...")

        # Concatenate all audio with natural pauses
        concatenate_audio(audio_segments, audio_path, gap=0.5)

    if progress_callback:
        progress_callback(20, "Calculating duration...")

    # Get total duration
    duration = get_audio_duration(audio_path)

    if progress_callback:
        progress_callback(25, f"Creating {int(duration)}s video...")

    # Video settings based on resolution
    fps = 24
    total_frames = int(duration * fps)

    if resolution == "tiktok" or resolution == "9:16":
        width, height = 1080, 1920  # Vertical for TikTok/Reels
    elif resolution == "720p":
        width, height = 1280, 720
    else:  # Default 1080p
        width, height = 1920, 1080

    is_vertical = height > width

    # Initialize animated scenery for category-based backgrounds
    scenery = None
    if bg_mode == "scenery":
        cat_info = get_category(content_category)
        scenery_style = cat_info.get('scenery', 'islamic_village')

        # Map content categories to scenery classes
        if content_category == "horror":
            scenery = HorrorScenery(width=width, height=height)
        elif content_category == "kids":
            scenery = KidsScenery(width=width, height=height)
        else:
            # Use default AnimatedScenery with appropriate style
            style_mapping = {
                'islamic_village': 'village_night',
                'horror_night': 'village_night',  # HorrorScenery handles this
                'sunny_village': 'village_night',  # KidsScenery handles this
                'noir_city': 'village_night',
                'sunrise_mountains': 'village_night',
                'ancient_ruins': 'village_night',
                'space': 'village_night',
                'moonlit_garden': 'village_night',
                'minimal': 'village_night',
                'cyber': 'village_night',
            }
            style = style_mapping.get(scenery_style, 'village_night')
            scenery = AnimatedScenery(width=width, height=height, style=style)

    # Text effect (simple string)
    selected_effect = text_effect.lower() if text_effect else "fade"

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

    # Font sizes adjusted for resolution
    if is_vertical:
        title_font = get_font(60, bold=True)
        arabic_font = get_font(48, bold=False)
        caption_font = get_font(42, bold=False)
    else:
        title_font = get_font(70, bold=True)
        arabic_font = get_font(58, bold=False)
        caption_font = get_font(50, bold=False)

    # Generate background elements - RANDOM seed for variety each video
    import time
    np.random.seed(int(time.time()) % 10000)  # Different each time

    # For dynamic mode, pre-compute themes for each caption
    caption_themes = []
    if bg_mode == "dynamic":
        for cap in caption_timing:
            theme = detect_theme(cap['original'])
            caption_themes.append({
                'theme': theme,
                'start': cap['start_frame'],
                'end': cap['end_frame'],
            })

    # Generate stars and particles using the animated_backgrounds module
    stars, particles = generate_stars_particles(width, height)

    # ============ CAPTION IMAGES (AI/Stock/Upload) ============
    caption_image_cache = {}  # Cache processed images for each caption

    if caption_images:
        # Use provided caption images
        cv = get_caption_visuals()
        for idx, img_path in caption_images.items():
            if Path(img_path).exists():
                caption_image_cache[int(idx)] = cv.prepare_for_video(
                    Path(img_path), width, height, darken=0.5, blur=2
                )

    elif auto_generate_images:
        # Auto-generate images for each caption
        if progress_callback:
            progress_callback(26, "Generating AI images for captions...")

        cv = get_caption_visuals()
        caption_texts = [cap['original'] for cap in caption_timing]

        def img_progress(pct, msg):
            if progress_callback:
                progress_callback(26 + int(pct * 0.15), msg)

        generated = cv.generate_all_visuals(
            caption_texts,
            style=image_style,
            mode='ai',
            progress_callback=img_progress
        )

        for idx, img_path in generated.items():
            caption_image_cache[idx] = cv.prepare_for_video(
                img_path, width, height, darken=0.5, blur=2
            )

    # Background color schemes for non-dynamic modes
    bg_change_frames = fps * 6
    bg_schemes = [
        {'r1': 5, 'g1': 8, 'b1': 28, 'r2': 20, 'g2': 35, 'b2': 65},
        {'r1': 15, 'g1': 5, 'b1': 25, 'r2': 45, 'g2': 20, 'b2': 55},
        {'r1': 5, 'g1': 15, 'b1': 20, 'r2': 15, 'g2': 40, 'b2': 50},
        {'r1': 10, 'g1': 10, 'b1': 25, 'r2': 30, 'g2': 30, 'b2': 55},
        {'r1': 8, 'g1': 5, 'b1': 18, 'r2': 25, 'g2': 15, 'b2': 45},
        {'r1': 3, 'g1': 8, 'b1': 15, 'r2': 10, 'g2': 25, 'b2': 40},
    ]

    # Generate frames
    for frame_num in range(total_frames):

        # ============ SCENERY BACKGROUND MODE (Category-based) ============
        if bg_mode == "scenery" and scenery:
            img = scenery.render_frame(frame_num)
            draw = ImageDraw.Draw(img)

        # ============ DYNAMIC BACKGROUND MODE ============
        elif bg_mode == "dynamic":
            # Find current and next theme based on caption timing
            current_theme = 'default'
            next_theme = None
            transition_progress = 0.0

            for i, ct in enumerate(caption_themes):
                if ct['start'] <= frame_num < ct['end']:
                    current_theme = ct['theme']
                    # Check for transition to next caption
                    transition_frames = fps // 2  # 0.5 second transition
                    if frame_num > ct['end'] - transition_frames and i + 1 < len(caption_themes):
                        next_theme = caption_themes[i + 1]['theme']
                        frames_left = ct['end'] - frame_num
                        transition_progress = 1 - (frames_left / transition_frames)
                    break

            # Use dynamic theme frame generator
            img = create_dynamic_theme_frame(
                width, height, frame_num,
                current_theme, next_theme, transition_progress,
                stars, particles
            )
            draw = ImageDraw.Draw(img)

        # ============ STATIC/ANIMATED BACKGROUND MODE ============
        else:
            img = Image.new('RGBA', (width, height), (0, 0, 0, 255))
            draw = ImageDraw.Draw(img)

            # Background gradient with smooth transition
            bg_idx = (frame_num // bg_change_frames) % len(bg_schemes)
            next_bg_idx = (bg_idx + 1) % len(bg_schemes)
            transition_progress = (frame_num % bg_change_frames) / bg_change_frames

            bg = bg_schemes[bg_idx]
            next_bg = bg_schemes[next_bg_idx]

            for y in range(height):
                py = y / height
                r1 = bg['r1'] + (next_bg['r1'] - bg['r1']) * transition_progress
                g1 = bg['g1'] + (next_bg['g1'] - bg['g1']) * transition_progress
                b1 = bg['b1'] + (next_bg['b1'] - bg['b1']) * transition_progress
                r2 = bg['r2'] + (next_bg['r2'] - bg['r2']) * transition_progress
                g2 = bg['g2'] + (next_bg['g2'] - bg['g2']) * transition_progress
                b2 = bg['b2'] + (next_bg['b2'] - bg['b2']) * transition_progress
                r = int(r1 + (r2 - r1) * py)
                g = int(g1 + (g2 - g1) * py)
                b = int(b1 + (b2 - b1) * py)
                draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

            # Draw stars with twinkling (for non-dynamic mode)
            for star in stars:
                twinkle = math.sin(frame_num * star['twinkle'] + star['x'] * 0.01)
                brightness = int(star['brightness'] + 40 * twinkle)
                brightness = max(80, min(255, brightness))
                x = star['x']
                y_pos = (star['y'] + frame_num * star['speed']) % height
                s = star['size']
                draw.ellipse(
                    [x - s, y_pos - s, x + s, y_pos + s],
                    fill=(brightness, brightness, int(brightness * 0.92), 255)
                )

            # Draw floating particles (fireflies) with proper alpha
            particle_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            particle_draw = ImageDraw.Draw(particle_layer)
            for p in particles:
                px = p['x']
                py = (p['y'] + frame_num * p['speed_y']) % height
                pa = p['alpha'] + int(30 * math.sin(frame_num * 0.04 + p['x'] * 0.01))
                pa = max(30, min(120, pa))  # More visible
                s = p['size']
                # Glow around particle
                particle_draw.ellipse(
                    [px - s*2, py - s*2, px + s*2, py + s*2],
                    fill=(255, 215, 0, pa // 3)
                )
                particle_draw.ellipse(
                    [px - s, py - s, px + s, py + s],
                    fill=(255, 230, 100, pa)
                )
            img = Image.alpha_composite(img, particle_layer)
            draw = ImageDraw.Draw(img)

            # Draw crescent moon with glow (using proper alpha compositing)
            moon_x, moon_y = width - 140, 100
            glow_intensity = 1 + 0.06 * math.sin(frame_num * 0.02)

            # Create glow layer for proper blending
            glow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            glow_draw = ImageDraw.Draw(glow_layer)

            for gs in range(int(55 * glow_intensity), int(38 * glow_intensity), -3):
                ga = int(40 * (55 - gs) / 17)  # Increased visibility
                glow_draw.ellipse(
                    [moon_x - gs, moon_y - gs, moon_x + gs, moon_y + gs],
                    fill=(255, 250, 200, ga)
                )

            # Composite glow onto main image
            img = Image.alpha_composite(img, glow_layer)
            draw = ImageDraw.Draw(img)

            # Moon body (bright)
            draw.ellipse(
                [moon_x - 40, moon_y - 40, moon_x + 40, moon_y + 40],
                fill=(255, 252, 238, 255)
            )
            # Cut out for crescent shape
            draw.ellipse(
                [moon_x - 5, moon_y - 48, moon_x + 52, moon_y + 48],
                fill=(int(bg['r1']), int(bg['g1']), int(bg['b1']), 255)
            )

        # Draw title (first 5 seconds with fade)
        if frame_num < fps * 5 and title_display:
            fade_in_frames = fps  # 1 second fade in
            fade_out_start = fps * 4  # Start fade out at 4 seconds

            if frame_num < fade_in_frames:
                alpha = int(255 * frame_num / fade_in_frames)
            elif frame_num > fade_out_start:
                alpha = int(255 * (fps * 5 - frame_num) / fps)
            else:
                alpha = 255

            try:
                bbox = draw.textbbox((0, 0), title_display, font=title_font)
                tw = bbox[2] - bbox[0]
                x = (width - tw) // 2
                y = 75

                # Shadow
                draw.text((x + 3, y + 3), title_display, fill=(0, 0, 0, int(alpha * 0.7)), font=title_font)
                # Main title
                draw.text((x, y), title_display, fill=(255, 255, 255, alpha), font=title_font)
            except Exception:
                pass

        # Find current caption and its index
        current_caption = None
        current_caption_idx = -1
        for idx, cap in enumerate(caption_timing):
            if cap['start_frame'] <= frame_num < cap['end_frame']:
                current_caption = cap
                current_caption_idx = idx
                break

        # ============ CAPTION IMAGE BACKGROUND ============
        if current_caption_idx >= 0 and current_caption_idx in caption_image_cache:
            # Blend caption image with current background
            caption_bg = caption_image_cache[current_caption_idx]

            # Calculate fade in/out for smooth transitions
            frame_in_caption = frame_num - current_caption['start_frame']
            total_caption_frames = current_caption['end_frame'] - current_caption['start_frame']
            fade_frames = min(fps // 2, total_caption_frames // 4)  # 0.5 sec or 25% of caption

            if frame_in_caption < fade_frames:
                # Fade in
                blend_alpha = frame_in_caption / fade_frames
            elif frame_in_caption > total_caption_frames - fade_frames:
                # Fade out
                blend_alpha = (total_caption_frames - frame_in_caption) / fade_frames
            else:
                blend_alpha = 1.0

            # Blend caption image over current background
            if blend_alpha > 0:
                img = Image.blend(img, caption_bg.convert('RGBA'), blend_alpha * 0.7)
                draw = ImageDraw.Draw(img)

        if current_caption:
            text = current_caption['text']
            is_arabic = current_caption['lang'] == 'arabic'
            frame_in_caption = frame_num - current_caption['start_frame']
            total_caption_frames = current_caption['end_frame'] - current_caption['start_frame']

            # Use simple caption renderer - ALL captions at CENTER for consistency
            if is_arabic:
                img = draw_arabic_caption(
                    img=img,
                    text=text,
                    font=arabic_font,
                    frame_in_caption=frame_in_caption,
                    total_frames=total_caption_frames,
                    position="center",  # Consistent positioning
                )
            else:
                img = draw_caption(
                    img=img,
                    text=text,
                    font=caption_font,
                    is_arabic=False,
                    frame_in_caption=frame_in_caption,
                    total_frames=total_caption_frames,
                    effect="fade",
                    position="center",  # Consistent positioning
                )

        # Save frame (convert RGBA to RGB for video)
        img_rgb = Image.new('RGB', img.size, (0, 0, 0))
        if len(img.split()) > 3:
            img_rgb.paste(img, mask=img.split()[3])
        else:
            img_rgb.paste(img)
        img_rgb.save(frames_dir / f"frame_{frame_num:05d}.png")

        # Progress update
        if frame_num % 48 == 0 and progress_callback:
            pct = 25 + int(50 * frame_num / total_frames)
            progress_callback(pct, f"Rendering frame {frame_num}/{total_frames}")

    if progress_callback:
        progress_callback(80, "Compiling video...")

    # Compile video with high quality settings
    temp_video = OUTPUT_DIR / "temp_render.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "medium",
        str(temp_video)
    ], capture_output=True)

    if progress_callback:
        progress_callback(85, "Processing audio...")

    # Mix background audio if specified
    final_audio_path = audio_path
    if background_audio:
        # Map background audio names to files
        bg_audio_dir = Path(__file__).parent / "assets" / "audio"
        bg_audio_mapping = {
            "wind": bg_audio_dir / "wind_breeze.mp3",
            "breeze": bg_audio_dir / "wind_breeze.mp3",
            "rain": bg_audio_dir / "rain.mp3",
            "fire": bg_audio_dir / "fire_crackle.mp3",
            "night": bg_audio_dir / "night_ambient.mp3",
        }

        # Get background audio path
        if background_audio in bg_audio_mapping:
            bg_audio_file = bg_audio_mapping[background_audio]
        else:
            bg_audio_file = Path(background_audio)

        if bg_audio_file.exists():
            if progress_callback:
                progress_callback(88, "Mixing background audio...")

            mixed_audio_path = OUTPUT_DIR / f"{output_name}_mixed_audio.mp3"

            # Mix voice with background audio (loop background, adjust volume)
            subprocess.run([
                "ffmpeg", "-y",
                "-i", str(audio_path),
                "-stream_loop", "-1",  # Loop background indefinitely
                "-i", str(bg_audio_file),
                "-filter_complex",
                f"[0:a]volume=1.0[voice];[1:a]volume={background_volume}[bg];[voice][bg]amix=inputs=2:duration=first:dropout_transition=2[out]",
                "-map", "[out]",
                "-c:a", "libmp3lame",
                "-q:a", "2",
                str(mixed_audio_path)
            ], capture_output=True)

            if mixed_audio_path.exists():
                final_audio_path = mixed_audio_path

    if progress_callback:
        progress_callback(90, "Adding audio to video...")

    # Add audio
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(temp_video),
        "-i", str(final_audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_path)
    ], capture_output=True)

    if progress_callback:
        progress_callback(95, "Cleaning up...")

    # Cleanup
    for f in frames_dir.glob("*.png"):
        f.unlink()
    if temp_video.exists():
        temp_video.unlink()

    if progress_callback:
        progress_callback(100, "Complete!")

    return output_path, audio_path


# Available text effects for UI
AVAILABLE_TEXT_EFFECTS = {
    "none": "No Effect - Static text",
    "fade": "Fade In/Out - Smooth opacity transition",
    "karaoke": "Karaoke - Word-by-word highlight",
    "typewriter": "Typewriter - Characters appear one by one",
    "slide_left": "Slide Left - Text slides in from right",
    "slide_right": "Slide Right - Text slides in from left",
    "slide_up": "Slide Up - Text slides in from bottom",
    "zoom": "Zoom In - Text zooms in at start",
}


if __name__ == "__main__":
    test_script = """رسول اللہ صلی اللہ علیہ وسلم نے فرمایا۔
تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ
اپنے بھائی کے سامنے مسکرانا صدقہ ہے۔
یہ حدیث جامع ترمذی میں ہے۔
مسکرانا بھی صدقہ ہے۔
سبسکرائب کریں۔"""

    def progress(pct, msg):
        print(f"[{pct}%] {msg}")

    print("Testing with karaoke effect...")
    video, audio = generate_video(
        script_urdu=test_script,
        title_urdu="مسکرانے کی طاقت",
        arabic_text="تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ",
        include_arabic_recitation=True,
        text_effect="karaoke",  # Test karaoke effect
        progress_callback=progress
    )
    print(f"\nVideo: {video}")
