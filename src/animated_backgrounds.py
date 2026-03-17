"""
Animated Backgrounds Module
Creates beautiful animated Islamic-themed backgrounds
With keyword-based dynamic theme changes - no characters (halal)
"""
import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from config import OUTPUT_DIR, ASSETS_DIR

# ============== KEYWORD-BASED THEMES ==============
# Islamic keyword to mood/theme mapping
KEYWORD_THEMES = {
    # Paradise/Reward - Green, golden, peaceful
    'جنت': 'paradise', 'جنة': 'paradise', 'نعمت': 'paradise',
    'اجر': 'paradise', 'ثواب': 'paradise', 'رحمت': 'paradise',
    'بخشش': 'paradise', 'مغفرت': 'paradise',

    # Warning - Red, orange, intense
    'جہنم': 'warning', 'عذاب': 'warning', 'گناہ': 'warning', 'ڈرو': 'warning',

    # Patience/Peace - Blue, calm
    'صبر': 'peace', 'سکون': 'peace', 'امن': 'peace', 'توکل': 'peace',

    # Love/Heart - Pink, warm
    'محبت': 'love', 'پیار': 'love', 'دل': 'love', 'ماں': 'love', 'والدین': 'love',

    # Prayer/Worship - Purple, spiritual
    'نماز': 'spiritual', 'عبادت': 'spiritual', 'دعا': 'spiritual',
    'ذکر': 'spiritual', 'تسبیح': 'spiritual',

    # Knowledge/Light - Yellow, bright
    'علم': 'knowledge', 'نور': 'knowledge', 'ہدایت': 'knowledge', 'قرآن': 'knowledge',

    # Gratitude - Gold, warm
    'شکر': 'gratitude', 'الحمد': 'gratitude', 'سبحان': 'gratitude',

    # Prophet/Respect - Emerald green
    'نبی': 'prophet', 'رسول': 'prophet', 'صلی اللہ': 'prophet', 'محمد': 'prophet',
}

# Theme color schemes
THEME_COLORS = {
    'paradise': {
        'bg_start': (5, 35, 15), 'bg_end': (15, 70, 35),
        'accent': (100, 200, 100), 'particles': (200, 255, 180), 'glow': (150, 255, 150),
    },
    'warning': {
        'bg_start': (35, 8, 5), 'bg_end': (70, 25, 10),
        'accent': (255, 120, 50), 'particles': (255, 180, 100), 'glow': (255, 100, 50),
    },
    'peace': {
        'bg_start': (5, 15, 40), 'bg_end': (20, 45, 90),
        'accent': (100, 150, 220), 'particles': (180, 210, 255), 'glow': (150, 200, 255),
    },
    'love': {
        'bg_start': (35, 12, 25), 'bg_end': (70, 30, 50),
        'accent': (220, 130, 170), 'particles': (255, 180, 210), 'glow': (255, 150, 200),
    },
    'spiritual': {
        'bg_start': (18, 8, 35), 'bg_end': (45, 25, 80),
        'accent': (160, 100, 200), 'particles': (200, 170, 255), 'glow': (180, 130, 255),
    },
    'knowledge': {
        'bg_start': (30, 25, 8), 'bg_end': (60, 55, 20),
        'accent': (255, 220, 100), 'particles': (255, 240, 180), 'glow': (255, 230, 150),
    },
    'gratitude': {
        'bg_start': (35, 28, 8), 'bg_end': (70, 60, 20),
        'accent': (255, 200, 80), 'particles': (255, 220, 150), 'glow': (255, 210, 120),
    },
    'prophet': {
        'bg_start': (5, 30, 15), 'bg_end': (15, 65, 35),
        'accent': (80, 180, 100), 'particles': (180, 255, 200), 'glow': (120, 220, 150),
    },
    'default': {
        'bg_start': (8, 15, 35), 'bg_end': (25, 45, 80),
        'accent': (100, 140, 200), 'particles': (200, 220, 255), 'glow': (150, 180, 255),
    },
}


def detect_theme(text: str) -> str:
    """Detect theme from text keywords"""
    if not text:
        return 'default'
    text_lower = text.lower()
    for keyword, theme in KEYWORD_THEMES.items():
        if keyword in text_lower:
            return theme
    return 'default'


def interpolate_color(c1, c2, t):
    """Smoothly interpolate between two colors"""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def create_animated_frames(
    duration: float,
    fps: int = 24,
    width: int = 1920,
    height: int = 1080,
    style: str = "islamic_geometric"
) -> Path:
    """
    Create animated background frames and compile to video

    Returns path to the background video
    """
    frames_dir = ASSETS_DIR / "frames"
    frames_dir.mkdir(exist_ok=True)

    total_frames = int(duration * fps)

    if style == "islamic_geometric":
        create_geometric_frames(frames_dir, total_frames, width, height)
    elif style == "particles":
        create_particle_frames(frames_dir, total_frames, width, height)
    elif style == "gradient_wave":
        create_gradient_wave_frames(frames_dir, total_frames, width, height)
    else:
        create_starfield_frames(frames_dir, total_frames, width, height)

    # Compile frames to video using ffmpeg
    output_path = ASSETS_DIR / "animated_bg.mp4"

    import subprocess
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        str(output_path)
    ]

    subprocess.run(cmd, capture_output=True)

    # Clean up frames
    for f in frames_dir.glob("*.png"):
        f.unlink()

    return output_path


def create_starfield_frames(frames_dir: Path, total_frames: int, width: int, height: int):
    """Create moving starfield animation"""

    # Generate random stars
    np.random.seed(42)
    num_stars = 200
    stars = []
    for _ in range(num_stars):
        stars.append({
            'x': np.random.randint(0, width),
            'y': np.random.randint(0, height),
            'size': np.random.randint(1, 4),
            'speed': np.random.uniform(0.5, 2),
            'brightness': np.random.randint(150, 255)
        })

    for frame_num in range(total_frames):
        # Create dark blue gradient background
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        # Gradient
        for y in range(height):
            r = int(5 + (15 - 5) * y / height)
            g = int(10 + (25 - 10) * y / height)
            b = int(30 + (50 - 30) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Draw and move stars
        for star in stars:
            # Twinkle effect
            brightness = star['brightness'] + int(30 * math.sin(frame_num * 0.1 + star['x']))
            brightness = max(100, min(255, brightness))

            x = star['x']
            y = (star['y'] + frame_num * star['speed']) % height

            color = (brightness, brightness, brightness)

            if star['size'] == 1:
                draw.point((x, y), fill=color)
            else:
                draw.ellipse([x-star['size'], y-star['size'],
                             x+star['size'], y+star['size']], fill=color)

        # Add subtle moon
        moon_x = width - 200
        moon_y = 150
        moon_phase = 0.7  # Crescent
        draw.ellipse([moon_x-60, moon_y-60, moon_x+60, moon_y+60],
                    fill=(255, 250, 230))
        # Crescent shadow
        draw.ellipse([moon_x-30, moon_y-60, moon_x+90, moon_y+60],
                    fill=(15, 25, 50))

        # Save frame
        img.save(frames_dir / f"frame_{frame_num:04d}.png")

        if frame_num % 50 == 0:
            print(f"  Creating frames: {frame_num}/{total_frames}")


def create_gradient_wave_frames(frames_dir: Path, total_frames: int, width: int, height: int):
    """Create flowing gradient wave animation"""

    for frame_num in range(total_frames):
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        # Animated gradient
        phase = frame_num * 0.05

        for y in range(height):
            # Wave effect in gradient
            wave = math.sin(y * 0.01 + phase) * 20

            # Base colors (dark blue to teal)
            progress = (y + wave) / height
            progress = max(0, min(1, progress))

            r = int(10 + 20 * progress)
            g = int(20 + 40 * progress)
            b = int(40 + 30 * progress)

            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Add floating particles
        np.random.seed(42)
        for i in range(50):
            px = (np.random.randint(0, width) + frame_num * 0.5) % width
            py = (np.random.randint(0, height) + frame_num * 0.3) % height

            alpha = int(100 + 50 * math.sin(frame_num * 0.1 + i))
            size = 2 + int(2 * math.sin(frame_num * 0.05 + i))

            draw.ellipse([px-size, py-size, px+size, py+size],
                        fill=(alpha, alpha + 30, alpha + 50))

        img.save(frames_dir / f"frame_{frame_num:04d}.png")

        if frame_num % 50 == 0:
            print(f"  Creating frames: {frame_num}/{total_frames}")


def create_geometric_frames(frames_dir: Path, total_frames: int, width: int, height: int):
    """Create Islamic geometric pattern animation"""

    for frame_num in range(total_frames):
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        # Dark background
        for y in range(height):
            r = int(15 + 10 * y / height)
            g = int(20 + 15 * y / height)
            b = int(35 + 20 * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Animated geometric pattern
        phase = frame_num * 0.02
        pattern_size = 100

        for cx in range(-pattern_size, width + pattern_size, pattern_size):
            for cy in range(-pattern_size, height + pattern_size, pattern_size):
                # Offset animation
                offset_x = 10 * math.sin(phase + cx * 0.01)
                offset_y = 10 * math.cos(phase + cy * 0.01)

                x = cx + offset_x
                y = cy + offset_y

                # Draw 8-pointed star (Islamic pattern)
                alpha = int(40 + 20 * math.sin(phase + cx + cy))
                color = (alpha, alpha + 20, alpha + 40)

                # Star points
                points = []
                for i in range(8):
                    angle = i * math.pi / 4 + phase * 0.5
                    r1 = 30
                    r2 = 15
                    if i % 2 == 0:
                        px = x + r1 * math.cos(angle)
                        py = y + r1 * math.sin(angle)
                    else:
                        px = x + r2 * math.cos(angle)
                        py = y + r2 * math.sin(angle)
                    points.append((px, py))

                if len(points) >= 3:
                    draw.polygon(points, outline=color)

        img.save(frames_dir / f"frame_{frame_num:04d}.png")

        if frame_num % 50 == 0:
            print(f"  Creating frames: {frame_num}/{total_frames}")


def create_particle_frames(frames_dir: Path, total_frames: int, width: int, height: int):
    """Create floating particle animation"""

    np.random.seed(42)
    num_particles = 100

    particles = []
    for _ in range(num_particles):
        particles.append({
            'x': np.random.randint(0, width),
            'y': np.random.randint(0, height),
            'vx': np.random.uniform(-0.5, 0.5),
            'vy': np.random.uniform(-1, -0.2),
            'size': np.random.randint(2, 8),
            'alpha': np.random.randint(50, 150)
        })

    for frame_num in range(total_frames):
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        # Gradient background
        for y in range(height):
            r = int(10 + 15 * y / height)
            g = int(15 + 25 * y / height)
            b = int(30 + 35 * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Update and draw particles
        for p in particles:
            p['x'] = (p['x'] + p['vx']) % width
            p['y'] = (p['y'] + p['vy']) % height

            # Pulsing alpha
            alpha = p['alpha'] + int(30 * math.sin(frame_num * 0.1 + p['x']))
            alpha = max(30, min(180, alpha))

            color = (alpha, alpha + 30, alpha + 60)

            x, y = int(p['x']), int(p['y'])
            s = p['size']
            draw.ellipse([x-s, y-s, x+s, y+s], fill=color)

        img.save(frames_dir / f"frame_{frame_num:04d}.png")

        if frame_num % 50 == 0:
            print(f"  Creating frames: {frame_num}/{total_frames}")


def create_typing_text_overlay(
    text_lines: list,
    duration: float,
    fps: int = 24,
    width: int = 1920,
    height: int = 1080
) -> list:
    """
    Create frames with typing text effect
    Returns list of frame paths
    """
    frames_dir = ASSETS_DIR / "text_frames"
    frames_dir.mkdir(exist_ok=True)

    total_frames = int(duration * fps)
    frames_per_line = total_frames // max(len(text_lines), 1)

    frame_paths = []

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    except:
        font = ImageFont.load_default()

    current_line_idx = 0
    chars_shown = 0

    for frame_num in range(total_frames):
        # Transparent image for overlay
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Calculate which line and how many chars to show
        line_progress = (frame_num % frames_per_line) / frames_per_line
        current_line_idx = min(frame_num // frames_per_line, len(text_lines) - 1)

        if current_line_idx < len(text_lines):
            current_line = text_lines[current_line_idx]
            chars_to_show = int(len(current_line) * line_progress)
            visible_text = current_line[:chars_to_show]

            # Add blinking cursor
            if frame_num % 12 < 6:
                visible_text += "|"

            # Draw text with shadow
            text_y = height - 200

            # Shadow
            draw.text((width//2 + 2, text_y + 2), visible_text,
                     fill=(0, 0, 0, 200), font=font, anchor="mm")

            # Main text
            draw.text((width//2, text_y), visible_text,
                     fill=(255, 255, 255, 255), font=font, anchor="mm")

        frame_path = frames_dir / f"text_{frame_num:04d}.png"
        img.save(frame_path)
        frame_paths.append(frame_path)

    return frame_paths


# Quick test function
def create_simple_animated_bg(duration: float, output_path: Path, style: str = "starfield") -> Path:
    """Create a simple animated background video"""

    print(f"Creating {style} animated background ({duration:.0f}s)...")

    frames_dir = ASSETS_DIR / "frames"
    frames_dir.mkdir(exist_ok=True)

    fps = 24
    total_frames = int(duration * fps)

    # Limit frames for performance (loop the video)
    max_frames = min(total_frames, 240)  # Max 10 seconds, then loop

    if style == "starfield":
        create_starfield_frames(frames_dir, max_frames, 1920, 1080)
    elif style == "particles":
        create_particle_frames(frames_dir, max_frames, 1920, 1080)
    elif style == "geometric":
        create_geometric_frames(frames_dir, max_frames, 1920, 1080)
    else:
        create_gradient_wave_frames(frames_dir, max_frames, 1920, 1080)

    print("  Compiling video...")

    import subprocess
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-t", str(duration),
        "-stream_loop", "-1",  # Loop if needed
        str(output_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Clean up frames
    for f in frames_dir.glob("*.png"):
        f.unlink()

    print(f"  Done: {output_path.name}")
    return output_path


def create_dynamic_theme_frame(
    width: int,
    height: int,
    frame_num: int,
    current_theme: str,
    next_theme: str = None,
    transition_progress: float = 0.0,
    stars: list = None,
    particles: list = None,
) -> Image.Image:
    """
    Create a single frame with dynamic theme-based background.
    Smoothly transitions between themes based on content.
    """
    img = Image.new('RGBA', (width, height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Get theme colors
    colors = THEME_COLORS.get(current_theme, THEME_COLORS['default'])

    # If transitioning, interpolate colors
    if next_theme and transition_progress > 0:
        next_colors = THEME_COLORS.get(next_theme, THEME_COLORS['default'])
        colors = {
            key: interpolate_color(colors[key], next_colors[key], transition_progress)
            for key in colors
        }

    # Draw gradient background
    for y in range(height):
        py = y / height
        r = int(colors['bg_start'][0] + (colors['bg_end'][0] - colors['bg_start'][0]) * py)
        g = int(colors['bg_start'][1] + (colors['bg_end'][1] - colors['bg_start'][1]) * py)
        b = int(colors['bg_start'][2] + (colors['bg_end'][2] - colors['bg_start'][2]) * py)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Draw light rays from top
    for i in range(6):
        base_x = (i + 0.5) * width / 6
        offset = 25 * math.sin(frame_num * 0.015 + i * 0.7)
        x = base_x + offset
        ray_width = 35 + 15 * math.sin(frame_num * 0.02 + i)
        alpha = int(12 + 8 * math.sin(frame_num * 0.02 + i * 0.4))

        points = [(x - ray_width/2, 0), (x + ray_width/2, 0),
                  (x + ray_width * 2.5, height), (x - ray_width * 2.5, height)]
        draw.polygon(points, fill=(*colors['glow'], alpha))

    # Draw animated Islamic geometric pattern (subtle)
    center_x, center_y = width // 2, height // 2
    rotation = frame_num * 0.003

    for ring in range(4, 9):
        radius = ring * min(width, height) // 14
        alpha = int(20 + 10 * math.sin(frame_num * 0.02 + ring))
        color = (*colors['accent'], alpha)

        points = []
        for i in range(8):
            angle = (i * math.pi / 4) + rotation
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            points.append((x, y))

        for i in range(8):
            draw.line([points[i], points[(i + 1) % 8]], fill=color, width=1)
            draw.line([points[i], points[(i + 3) % 8]], fill=color, width=1)

    # Draw stars with theme-colored twinkling
    if stars:
        for star in stars:
            twinkle = math.sin(frame_num * star['twinkle'] + star['x'] * 0.01)
            brightness = int(star['brightness'] + 50 * twinkle)
            brightness = max(80, min(255, brightness))

            x = star['x']
            y_pos = (star['y'] + frame_num * star['speed']) % height
            s = star['size']

            # Mix star color with theme
            sr = int(brightness * 0.6 + colors['particles'][0] * 0.4 / 255 * brightness)
            sg = int(brightness * 0.6 + colors['particles'][1] * 0.4 / 255 * brightness)
            sb = int(brightness * 0.6 + colors['particles'][2] * 0.4 / 255 * brightness)

            draw.ellipse([x - s, y_pos - s, x + s, y_pos + s], fill=(sr, sg, sb, 255))

    # Draw floating particles with theme color
    if particles:
        for p in particles:
            px = p['x']
            py_pos = (p['y'] + frame_num * p['speed_y']) % height
            pa = p['alpha'] + int(15 * math.sin(frame_num * 0.035 + p['x'] * 0.01))
            pa = max(15, min(70, pa))

            pc = (*colors['particles'], pa)
            draw.ellipse([px - p['size'], py_pos - p['size'],
                         px + p['size'], py_pos + p['size']], fill=pc)

    # Draw crescent moon with theme-tinted glow
    moon_x, moon_y = width - 130, 95
    glow_intensity = 1 + 0.08 * math.sin(frame_num * 0.018)

    for gs in range(int(50 * glow_intensity), int(35 * glow_intensity), -2):
        ga = int(15 * (50 - gs) / 15)
        glow_color = (
            int(255 * 0.7 + colors['glow'][0] * 0.3),
            int(250 * 0.7 + colors['glow'][1] * 0.3),
            int(220 * 0.7 + colors['glow'][2] * 0.3),
            ga
        )
        draw.ellipse([moon_x - gs, moon_y - gs, moon_x + gs, moon_y + gs], fill=glow_color)

    draw.ellipse([moon_x - 35, moon_y - 35, moon_x + 35, moon_y + 35], fill=(255, 252, 240, 255))
    draw.ellipse([moon_x - 3, moon_y - 42, moon_x + 48, moon_y + 42],
                 fill=(colors['bg_start'][0], colors['bg_start'][1], colors['bg_start'][2], 255))

    return img


def generate_stars_particles(width: int, height: int, seed: int = None):
    """Generate stars and particles for animation"""
    if seed is None:
        import time
        seed = int(time.time()) % 10000
    np.random.seed(seed)

    stars = [{
        'x': np.random.randint(0, width),
        'y': np.random.randint(0, height),
        'size': np.random.randint(1, 4),
        'speed': np.random.uniform(0.1, 0.4),
        'brightness': np.random.randint(150, 255),
        'twinkle': np.random.uniform(0.03, 0.08)
    } for _ in range(180)]

    particles = [{
        'x': np.random.randint(0, width),
        'y': np.random.randint(0, height),
        'size': np.random.randint(2, 5),
        'speed_y': np.random.uniform(-0.35, -0.1),
        'alpha': np.random.randint(25, 55)
    } for _ in range(35)]

    return stars, particles


if __name__ == "__main__":
    # Test
    test_path = ASSETS_DIR / "test_animated.mp4"
    create_simple_animated_bg(10, test_path, "starfield")
    print(f"Test video created: {test_path}")

    # Test theme detection
    test_texts = ["جنت کی نعمتیں", "صبر کرو", "نماز پڑھو", "ماں کا مقام"]
    for t in test_texts:
        print(f"'{t}' -> {detect_theme(t)}")
