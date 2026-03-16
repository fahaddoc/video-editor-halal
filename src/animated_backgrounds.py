"""
Animated Backgrounds Module
Creates beautiful animated Islamic-themed backgrounds
"""
import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from config import OUTPUT_DIR, ASSETS_DIR


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


if __name__ == "__main__":
    # Test
    test_path = ASSETS_DIR / "test_animated.mp4"
    create_simple_animated_bg(10, test_path, "starfield")
    print(f"Test video created: {test_path}")
