"""
Animated Scenery Backgrounds
Beautiful Islamic night scenes - no faces/characters
Stars, moon, houses, mosques, minarets - all animated
"""
import math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from typing import List, Dict, Tuple


class AnimatedScenery:
    """Creates beautiful animated scenery backgrounds"""

    def __init__(self, width: int = 1920, height: int = 1080, style: str = "village_night"):
        self.width = width
        self.height = height
        self.style = style

        # Generate scene elements
        np.random.seed(int(width * height) % 10000)
        self._init_stars()
        self._init_buildings()
        self._init_particles()

    def _init_stars(self):
        """Initialize twinkling stars"""
        self.stars = []
        # More stars at top, fewer near horizon
        for _ in range(300):
            y = np.random.randint(0, int(self.height * 0.6))
            self.stars.append({
                'x': np.random.randint(0, self.width),
                'y': y,
                'size': np.random.uniform(0.5, 2.5),
                'brightness': np.random.uniform(0.4, 1.0),
                'twinkle_speed': np.random.uniform(0.02, 0.08),
                'twinkle_offset': np.random.uniform(0, 2 * math.pi),
            })

    def _init_buildings(self):
        """Initialize building silhouettes"""
        self.buildings = []
        horizon_y = int(self.height * 0.65)

        # Create varied building silhouettes
        x = 0
        while x < self.width + 100:
            building_type = np.random.choice(['house', 'mosque', 'minaret', 'tree', 'dome'])

            if building_type == 'house':
                w = np.random.randint(60, 120)
                h = np.random.randint(80, 150)
                self.buildings.append({
                    'type': 'house',
                    'x': x,
                    'y': horizon_y,
                    'width': w,
                    'height': h,
                    'windows': self._generate_windows(x, horizon_y, w, h),
                    'has_chimney': np.random.random() > 0.6,
                })
                x += w + np.random.randint(10, 40)

            elif building_type == 'mosque':
                w = np.random.randint(150, 250)
                h = np.random.randint(120, 180)
                self.buildings.append({
                    'type': 'mosque',
                    'x': x,
                    'y': horizon_y,
                    'width': w,
                    'height': h,
                    'dome_height': np.random.randint(40, 70),
                    'windows': self._generate_windows(x, horizon_y, w, h, mosque=True),
                })
                x += w + np.random.randint(30, 60)

            elif building_type == 'minaret':
                w = np.random.randint(25, 40)
                h = np.random.randint(150, 220)
                self.buildings.append({
                    'type': 'minaret',
                    'x': x,
                    'y': horizon_y,
                    'width': w,
                    'height': h,
                })
                x += w + np.random.randint(20, 50)

            elif building_type == 'tree':
                w = np.random.randint(40, 80)
                h = np.random.randint(100, 180)
                self.buildings.append({
                    'type': 'tree',
                    'x': x,
                    'y': horizon_y,
                    'width': w,
                    'height': h,
                })
                x += w + np.random.randint(15, 40)

            elif building_type == 'dome':
                w = np.random.randint(80, 140)
                h = np.random.randint(60, 100)
                self.buildings.append({
                    'type': 'dome',
                    'x': x,
                    'y': horizon_y,
                    'width': w,
                    'height': h,
                })
                x += w + np.random.randint(20, 50)

    def _generate_windows(self, bx, by, bw, bh, mosque=False):
        """Generate window positions for buildings"""
        windows = []
        if mosque:
            # Arched windows for mosque
            num_windows = np.random.randint(3, 6)
            for i in range(num_windows):
                wx = bx + int(bw * (i + 1) / (num_windows + 1))
                wy = by - int(bh * 0.4)
                windows.append({
                    'x': wx, 'y': wy,
                    'width': 15, 'height': 25,
                    'arched': True,
                    'light_phase': np.random.uniform(0, 2 * math.pi),
                })
        else:
            # Square windows for houses
            rows = np.random.randint(1, 3)
            cols = np.random.randint(2, 4)
            for row in range(rows):
                for col in range(cols):
                    wx = bx + int(bw * (col + 1) / (cols + 1))
                    wy = by - int(bh * (row + 1) / (rows + 2))
                    windows.append({
                        'x': wx, 'y': wy,
                        'width': 12, 'height': 15,
                        'arched': False,
                        'light_phase': np.random.uniform(0, 2 * math.pi),
                    })
        return windows

    def _init_particles(self):
        """Initialize floating particles (fireflies, dust, etc.)"""
        self.particles = []
        for _ in range(50):
            self.particles.append({
                'x': np.random.randint(0, self.width),
                'y': np.random.randint(int(self.height * 0.4), self.height),
                'size': np.random.uniform(1, 3),
                'speed_x': np.random.uniform(-0.3, 0.3),
                'speed_y': np.random.uniform(-0.2, 0.2),
                'brightness': np.random.uniform(0.3, 0.8),
                'phase': np.random.uniform(0, 2 * math.pi),
            })

    def render_frame(self, frame_num: int) -> Image.Image:
        """Render a single frame of the animated scenery"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)

        # Draw sky gradient
        self._draw_sky(draw, frame_num)

        # Draw stars
        self._draw_stars(draw, frame_num)

        # Draw moon
        self._draw_moon(draw, frame_num)

        # Draw distant mountains/hills silhouette
        self._draw_hills(draw, frame_num)

        # Draw buildings silhouette
        self._draw_buildings(draw, frame_num)

        # Draw ground
        self._draw_ground(draw, frame_num)

        # Draw particles (fireflies)
        self._draw_particles(draw, frame_num)

        return img

    def _draw_sky(self, draw, frame_num):
        """Draw animated gradient sky"""
        # Subtle color shift over time
        shift = math.sin(frame_num * 0.005) * 10

        for y in range(int(self.height * 0.7)):
            progress = y / (self.height * 0.7)

            # Night sky colors - deep blue to purple
            r = int(5 + 15 * progress + shift * 0.3)
            g = int(8 + 20 * progress)
            b = int(30 + 40 * progress - shift * 0.2)

            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))

    def _draw_stars(self, draw, frame_num):
        """Draw twinkling stars"""
        for star in self.stars:
            # Twinkle effect
            twinkle = math.sin(frame_num * star['twinkle_speed'] + star['twinkle_offset'])
            brightness = star['brightness'] * (0.6 + 0.4 * twinkle)

            if brightness > 0.2:
                color_val = int(255 * brightness)
                size = star['size'] * (0.8 + 0.2 * twinkle)

                # Star glow
                if size > 1.5:
                    glow_size = size * 2
                    glow_alpha = int(50 * brightness)
                    draw.ellipse([
                        star['x'] - glow_size, star['y'] - glow_size,
                        star['x'] + glow_size, star['y'] + glow_size
                    ], fill=(color_val, color_val, int(color_val * 0.9), glow_alpha))

                # Star core
                draw.ellipse([
                    star['x'] - size, star['y'] - size,
                    star['x'] + size, star['y'] + size
                ], fill=(color_val, color_val, int(color_val * 0.95), 255))

    def _draw_moon(self, draw, frame_num):
        """Draw glowing crescent moon"""
        moon_x = self.width - 180
        moon_y = 120
        moon_size = 60

        # Gentle floating animation
        float_y = int(5 * math.sin(frame_num * 0.02))
        moon_y += float_y

        # Moon glow - multiple layers
        glow_pulse = 1 + 0.05 * math.sin(frame_num * 0.03)
        for i in range(8):
            glow_size = moon_size + (8 - i) * 15 * glow_pulse
            glow_alpha = int(15 + i * 3)
            draw.ellipse([
                moon_x - glow_size, moon_y - glow_size,
                moon_x + glow_size, moon_y + glow_size
            ], fill=(255, 250, 220, glow_alpha))

        # Moon body
        draw.ellipse([
            moon_x - moon_size, moon_y - moon_size,
            moon_x + moon_size, moon_y + moon_size
        ], fill=(255, 253, 245, 255))

        # Crescent shadow
        shadow_offset = moon_size * 0.4
        draw.ellipse([
            moon_x - moon_size + shadow_offset, moon_y - moon_size - 5,
            moon_x + moon_size + shadow_offset, moon_y + moon_size - 5
        ], fill=(15, 20, 40, 255))

    def _draw_hills(self, draw, frame_num):
        """Draw distant hills/mountains silhouette"""
        horizon_y = int(self.height * 0.65)

        # Draw wavy hills
        points = [(0, horizon_y)]
        x = 0
        while x <= self.width:
            hill_height = 30 + 20 * math.sin(x * 0.005) + 15 * math.sin(x * 0.012)
            points.append((x, horizon_y - int(hill_height)))
            x += 20
        points.append((self.width, horizon_y))
        points.append((self.width, self.height))
        points.append((0, self.height))

        draw.polygon(points, fill=(15, 20, 35, 255))

    def _draw_buildings(self, draw, frame_num):
        """Draw building silhouettes with animated windows"""
        for building in self.buildings:
            bx = building['x']
            by = building['y']
            bw = building['width']
            bh = building['height']

            if building['type'] == 'house':
                # House body
                draw.rectangle([bx, by - bh, bx + bw, by], fill=(10, 15, 25, 255))

                # Roof (triangle)
                roof_height = bh // 3
                draw.polygon([
                    (bx - 10, by - bh),
                    (bx + bw // 2, by - bh - roof_height),
                    (bx + bw + 10, by - bh)
                ], fill=(8, 12, 20, 255))

                # Chimney
                if building.get('has_chimney'):
                    cx = bx + bw * 3 // 4
                    draw.rectangle([cx, by - bh - roof_height + 10, cx + 15, by - bh],
                                  fill=(10, 15, 25, 255))

            elif building['type'] == 'mosque':
                # Mosque body
                draw.rectangle([bx, by - bh, bx + bw, by], fill=(12, 18, 30, 255))

                # Main dome
                dome_h = building['dome_height']
                dome_cx = bx + bw // 2
                draw.arc([dome_cx - bw//3, by - bh - dome_h, dome_cx + bw//3, by - bh + dome_h//2],
                        0, 180, fill=(15, 22, 35, 255), width=100)
                draw.pieslice([dome_cx - bw//3, by - bh - dome_h, dome_cx + bw//3, by - bh + dome_h//2],
                             180, 360, fill=(12, 18, 30, 255))

                # Crescent on dome
                crescent_y = by - bh - dome_h - 15
                draw.arc([dome_cx - 10, crescent_y - 10, dome_cx + 10, crescent_y + 10],
                        220, 320, fill=(255, 215, 0, 200), width=2)

            elif building['type'] == 'minaret':
                # Minaret tower
                draw.rectangle([bx, by - bh, bx + bw, by], fill=(12, 18, 30, 255))

                # Minaret top (pointed)
                draw.polygon([
                    (bx, by - bh),
                    (bx + bw // 2, by - bh - 30),
                    (bx + bw, by - bh)
                ], fill=(15, 22, 35, 255))

                # Crescent on top
                draw.arc([bx + bw//2 - 8, by - bh - 45, bx + bw//2 + 8, by - bh - 30],
                        220, 320, fill=(255, 215, 0, 180), width=2)

            elif building['type'] == 'tree':
                # Tree trunk
                trunk_w = bw // 4
                draw.rectangle([bx + bw//2 - trunk_w//2, by - bh//3, bx + bw//2 + trunk_w//2, by],
                              fill=(8, 12, 20, 255))

                # Tree foliage (layered circles)
                for i in range(3):
                    cy = by - bh//3 - i * bh//5
                    size = bw//2 - i * 10
                    draw.ellipse([bx + bw//2 - size, cy - size, bx + bw//2 + size, cy + size],
                                fill=(10, 18, 28, 255))

            elif building['type'] == 'dome':
                # Small dome building
                draw.rectangle([bx, by - bh//2, bx + bw, by], fill=(12, 18, 30, 255))
                draw.pieslice([bx, by - bh, bx + bw, by], 180, 360, fill=(15, 22, 38, 255))

            # Draw windows with animated glow
            for window in building.get('windows', []):
                # Window light flicker
                flicker = 0.7 + 0.3 * math.sin(frame_num * 0.05 + window['light_phase'])

                # Warm window glow
                glow_color = (255, 200, 100, int(60 * flicker))
                window_color = (255, 220, 150, int(200 * flicker))

                wx, wy = window['x'], window['y']
                ww, wh = window['width'], window['height']

                # Window glow
                draw.ellipse([wx - ww, wy - wh, wx + ww, wy + wh], fill=glow_color)

                # Window
                if window['arched']:
                    draw.rectangle([wx - ww//2, wy - wh//2, wx + ww//2, wy + wh//2], fill=window_color)
                    draw.pieslice([wx - ww//2, wy - wh, wx + ww//2, wy], 180, 360, fill=window_color)
                else:
                    draw.rectangle([wx - ww//2, wy - wh//2, wx + ww//2, wy + wh//2], fill=window_color)

    def _draw_ground(self, draw, frame_num):
        """Draw ground/foreground"""
        horizon_y = int(self.height * 0.65)

        # Ground gradient
        for y in range(horizon_y, self.height):
            progress = (y - horizon_y) / (self.height - horizon_y)
            r = int(8 + 5 * progress)
            g = int(12 + 8 * progress)
            b = int(20 + 10 * progress)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))

    def _draw_particles(self, draw, frame_num):
        """Draw floating particles (fireflies)"""
        for p in self.particles:
            # Animate position
            px = (p['x'] + frame_num * p['speed_x']) % self.width
            py = p['y'] + math.sin(frame_num * 0.03 + p['phase']) * 10

            # Glow effect
            glow = 0.5 + 0.5 * math.sin(frame_num * 0.08 + p['phase'])
            brightness = p['brightness'] * glow

            if brightness > 0.3:
                alpha = int(150 * brightness)
                size = p['size'] * (0.8 + 0.4 * glow)

                # Warm firefly color
                color = (255, 230, 150, alpha)
                draw.ellipse([px - size * 2, py - size * 2, px + size * 2, py + size * 2],
                            fill=(255, 220, 100, int(alpha * 0.3)))
                draw.ellipse([px - size, py - size, px + size, py + size], fill=color)


def create_scenery_video(
    output_path: str,
    duration: float = 10,
    fps: int = 24,
    width: int = 1920,
    height: int = 1080,
    style: str = "village_night"
) -> str:
    """Create a scenery background video"""
    import subprocess
    from pathlib import Path

    frames_dir = Path("assets/scenery_frames")
    frames_dir.mkdir(exist_ok=True)

    # Clean old frames
    for f in frames_dir.glob("*.png"):
        f.unlink()

    scenery = AnimatedScenery(width, height, style)
    total_frames = int(duration * fps)

    print(f"Rendering {total_frames} frames...")
    for frame in range(total_frames):
        img = scenery.render_frame(frame)

        # Convert to RGB
        img_rgb = Image.new('RGB', img.size, (0, 0, 0))
        img_rgb.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
        img_rgb.save(frames_dir / f"frame_{frame:05d}.png")

        if frame % 48 == 0:
            print(f"  Frame {frame}/{total_frames}")

    print("Compiling video...")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", "-preset", "medium",
        str(output_path)
    ], capture_output=True)

    # Cleanup
    for f in frames_dir.glob("*.png"):
        f.unlink()

    print(f"✓ Video created: {output_path}")
    return output_path


class HorrorScenery(AnimatedScenery):
    """Spooky horror scenery - abandoned houses, fog, bats"""

    def _init_stars(self):
        """Fewer, dimmer stars for horror"""
        self.stars = []
        for _ in range(100):
            y = np.random.randint(0, int(self.height * 0.5))
            self.stars.append({
                'x': np.random.randint(0, self.width),
                'y': y,
                'size': np.random.uniform(0.3, 1.5),
                'brightness': np.random.uniform(0.2, 0.5),
                'twinkle_speed': np.random.uniform(0.01, 0.03),
                'twinkle_offset': np.random.uniform(0, 2 * math.pi),
            })

        # Add bats
        self.bats = []
        for _ in range(15):
            self.bats.append({
                'x': np.random.randint(0, self.width),
                'y': np.random.randint(50, int(self.height * 0.4)),
                'speed': np.random.uniform(2, 5),
                'wing_speed': np.random.uniform(0.3, 0.5),
                'size': np.random.randint(8, 20),
            })

    def _init_buildings(self):
        """Creepy abandoned buildings"""
        self.buildings = []
        horizon_y = int(self.height * 0.65)
        x = 0

        while x < self.width + 100:
            building_type = np.random.choice(['haunted_house', 'dead_tree', 'grave', 'ruins'])

            if building_type == 'haunted_house':
                w = np.random.randint(100, 180)
                h = np.random.randint(150, 220)
                self.buildings.append({
                    'type': 'haunted_house', 'x': x, 'y': horizon_y,
                    'width': w, 'height': h,
                    'windows': self._generate_creepy_windows(x, horizon_y, w, h),
                })
                x += w + np.random.randint(50, 100)

            elif building_type == 'dead_tree':
                w = np.random.randint(60, 100)
                h = np.random.randint(150, 250)
                self.buildings.append({
                    'type': 'dead_tree', 'x': x, 'y': horizon_y,
                    'width': w, 'height': h,
                })
                x += w + np.random.randint(30, 60)

            elif building_type == 'grave':
                w = np.random.randint(30, 50)
                h = np.random.randint(40, 70)
                self.buildings.append({
                    'type': 'grave', 'x': x, 'y': horizon_y,
                    'width': w, 'height': h,
                })
                x += w + np.random.randint(20, 40)

            elif building_type == 'ruins':
                w = np.random.randint(80, 140)
                h = np.random.randint(80, 120)
                self.buildings.append({
                    'type': 'ruins', 'x': x, 'y': horizon_y,
                    'width': w, 'height': h,
                })
                x += w + np.random.randint(40, 80)

    def _generate_creepy_windows(self, bx, by, bw, bh):
        """Windows with occasional flickering light"""
        windows = []
        rows, cols = 2, 3
        for row in range(rows):
            for col in range(cols):
                if np.random.random() > 0.4:  # Some windows broken/dark
                    wx = bx + int(bw * (col + 1) / (cols + 1))
                    wy = by - int(bh * (row + 1) / (rows + 2))
                    windows.append({
                        'x': wx, 'y': wy, 'width': 15, 'height': 20,
                        'light_phase': np.random.uniform(0, 2 * math.pi),
                        'flicker': np.random.random() > 0.7,
                    })
        return windows

    def _draw_sky(self, draw, frame_num):
        """Dark, ominous sky"""
        for y in range(int(self.height * 0.7)):
            progress = y / (self.height * 0.7)
            r = int(8 + 10 * progress)
            g = int(5 + 8 * progress)
            b = int(15 + 15 * progress)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))

        # Add fog layers
        self._draw_fog(draw, frame_num)

    def _draw_fog(self, draw, frame_num):
        """Animated rolling fog"""
        for layer in range(3):
            fog_y = int(self.height * (0.5 + layer * 0.1))
            fog_alpha = 20 - layer * 5

            for x in range(0, self.width, 50):
                offset = math.sin(frame_num * 0.02 + x * 0.01 + layer) * 30
                fog_width = 100 + 50 * math.sin(x * 0.02)

                draw.ellipse([
                    x - fog_width + offset, fog_y - 30,
                    x + fog_width + offset, fog_y + 30
                ], fill=(100, 100, 120, fog_alpha))

    def _draw_moon(self, draw, frame_num):
        """Blood moon or hidden moon"""
        moon_x = self.width - 200
        moon_y = 100
        moon_size = 50

        # Occasional cloud passing
        cloud_pass = (frame_num % 300) / 300
        if 0.3 < cloud_pass < 0.7:
            return  # Moon hidden

        # Reddish moon
        for i in range(5):
            glow_size = moon_size + (5 - i) * 10
            glow_alpha = int(10 + i * 3)
            draw.ellipse([
                moon_x - glow_size, moon_y - glow_size,
                moon_x + glow_size, moon_y + glow_size
            ], fill=(150, 80, 80, glow_alpha))

        draw.ellipse([
            moon_x - moon_size, moon_y - moon_size,
            moon_x + moon_size, moon_y + moon_size
        ], fill=(200, 150, 140, 255))

    def _draw_buildings(self, draw, frame_num):
        """Draw creepy buildings"""
        for building in self.buildings:
            bx, by = building['x'], building['y']
            bw, bh = building['width'], building['height']

            if building['type'] == 'haunted_house':
                # Crooked house
                draw.polygon([
                    (bx, by), (bx + 5, by - bh),
                    (bx + bw - 5, by - bh), (bx + bw, by)
                ], fill=(15, 12, 20, 255))

                # Broken roof
                draw.polygon([
                    (bx - 10, by - bh), (bx + bw//2 - 10, by - bh - bh//2),
                    (bx + bw + 10, by - bh)
                ], fill=(10, 8, 15, 255))

                # Windows with creepy flicker
                for window in building.get('windows', []):
                    if window.get('flicker'):
                        flicker = 0.3 + 0.7 * (math.sin(frame_num * 0.1 + window['light_phase']) > 0.8)
                    else:
                        flicker = 0.2

                    wx, wy = window['x'], window['y']
                    color = (int(200 * flicker), int(150 * flicker), int(50 * flicker), int(150 * flicker))
                    draw.rectangle([wx - 7, wy - 10, wx + 7, wy + 10], fill=color)

            elif building['type'] == 'dead_tree':
                # Trunk
                draw.polygon([
                    (bx + bw//2 - 10, by), (bx + bw//2 - 5, by - bh),
                    (bx + bw//2 + 5, by - bh), (bx + bw//2 + 10, by)
                ], fill=(20, 15, 10, 255))

                # Bare branches
                for i in range(5):
                    branch_y = by - bh * (0.3 + i * 0.15)
                    branch_len = bw * (0.3 + np.random.random() * 0.3)
                    direction = 1 if i % 2 == 0 else -1
                    draw.line([
                        (bx + bw//2, branch_y),
                        (bx + bw//2 + direction * branch_len, branch_y - 20)
                    ], fill=(20, 15, 10, 255), width=3)

            elif building['type'] == 'grave':
                # Tombstone
                draw.rectangle([bx, by - bh, bx + bw, by], fill=(40, 40, 50, 255))
                draw.arc([bx, by - bh - bw//2, bx + bw, by - bh + bw//2],
                        180, 360, fill=(40, 40, 50, 255), width=50)

            elif building['type'] == 'ruins':
                # Broken walls
                for i in range(3):
                    wall_h = bh * np.random.uniform(0.3, 1.0)
                    wall_x = bx + i * bw // 3
                    draw.rectangle([wall_x, by - wall_h, wall_x + bw//4, by],
                                  fill=(25, 22, 30, 255))

    def _draw_particles(self, draw, frame_num):
        """Draw bats instead of fireflies"""
        for bat in self.bats:
            bx = (bat['x'] + frame_num * bat['speed']) % self.width
            by = bat['y'] + math.sin(frame_num * 0.05) * 20

            # Wing flap
            wing_angle = math.sin(frame_num * bat['wing_speed']) * 0.5
            size = bat['size']

            # Simple bat shape
            draw.polygon([
                (bx, by),
                (bx - size * (1 + wing_angle), by - size//2),
                (bx - size//2, by),
                (bx, by + size//3),
                (bx + size//2, by),
                (bx + size * (1 + wing_angle), by - size//2),
            ], fill=(20, 15, 25, 200))


class KidsScenery(AnimatedScenery):
    """Bright, colorful scenery for kids content"""

    def _init_stars(self):
        """Clouds instead of stars"""
        self.clouds = []
        for _ in range(8):
            self.clouds.append({
                'x': np.random.randint(0, self.width),
                'y': np.random.randint(50, int(self.height * 0.3)),
                'size': np.random.randint(80, 150),
                'speed': np.random.uniform(0.2, 0.5),
            })

        # Butterflies
        self.butterflies = []
        for _ in range(12):
            self.butterflies.append({
                'x': np.random.randint(0, self.width),
                'y': np.random.randint(int(self.height * 0.3), int(self.height * 0.7)),
                'color': np.random.choice(['pink', 'yellow', 'blue', 'purple']),
                'speed': np.random.uniform(1, 2),
                'wing_speed': np.random.uniform(0.2, 0.4),
                'size': np.random.randint(10, 20),
            })

        self.stars = []  # No stars in daytime

    def _init_buildings(self):
        """Cute houses and trees"""
        self.buildings = []
        horizon_y = int(self.height * 0.7)
        x = 50

        while x < self.width - 50:
            building_type = np.random.choice(['cute_house', 'tree', 'flower', 'bush'])

            if building_type == 'cute_house':
                w = np.random.randint(80, 120)
                h = np.random.randint(80, 120)
                color = np.random.choice(['red', 'blue', 'yellow', 'green', 'pink'])
                self.buildings.append({
                    'type': 'cute_house', 'x': x, 'y': horizon_y,
                    'width': w, 'height': h, 'color': color,
                })
                x += w + np.random.randint(60, 100)

            elif building_type == 'tree':
                w = np.random.randint(50, 80)
                h = np.random.randint(100, 150)
                self.buildings.append({
                    'type': 'tree', 'x': x, 'y': horizon_y,
                    'width': w, 'height': h,
                })
                x += w + np.random.randint(30, 60)

            elif building_type == 'flower':
                for _ in range(np.random.randint(3, 6)):
                    self.buildings.append({
                        'type': 'flower', 'x': x + np.random.randint(-20, 20),
                        'y': horizon_y, 'width': 20, 'height': np.random.randint(30, 60),
                        'color': np.random.choice(['red', 'yellow', 'pink', 'purple']),
                    })
                x += 50

    def _draw_sky(self, draw, frame_num):
        """Bright blue sky gradient"""
        for y in range(int(self.height * 0.7)):
            progress = y / (self.height * 0.7)
            r = int(135 + 65 * progress)
            g = int(200 + 30 * progress)
            b = 255
            draw.line([(0, y), (self.width, y)], fill=(r, g, b, 255))

        # Draw sun
        self._draw_sun(draw, frame_num)

        # Draw clouds
        for cloud in self.clouds:
            cx = (cloud['x'] + frame_num * cloud['speed']) % (self.width + 200) - 100
            cy = cloud['y']
            size = cloud['size']

            # Fluffy cloud from circles
            for i in range(4):
                offset_x = (i - 1.5) * size * 0.4
                offset_y = math.sin(i * 1.5) * size * 0.2
                draw.ellipse([
                    cx + offset_x - size * 0.4, cy + offset_y - size * 0.3,
                    cx + offset_x + size * 0.4, cy + offset_y + size * 0.3
                ], fill=(255, 255, 255, 230))

    def _draw_sun(self, draw, frame_num):
        """Happy sun (no face)"""
        sun_x, sun_y = 150, 120
        sun_size = 60

        # Sun rays
        ray_count = 12
        for i in range(ray_count):
            angle = frame_num * 0.01 + i * 2 * math.pi / ray_count
            ray_len = sun_size + 30 + 10 * math.sin(frame_num * 0.1 + i)

            end_x = sun_x + ray_len * math.cos(angle)
            end_y = sun_y + ray_len * math.sin(angle)

            draw.line([(sun_x, sun_y), (end_x, end_y)], fill=(255, 220, 100, 200), width=4)

        # Sun body
        draw.ellipse([
            sun_x - sun_size, sun_y - sun_size,
            sun_x + sun_size, sun_y + sun_size
        ], fill=(255, 230, 100, 255))

    def _draw_moon(self, draw, frame_num):
        """No moon in daytime"""
        pass

    def _draw_hills(self, draw, frame_num):
        """Green rolling hills"""
        horizon_y = int(self.height * 0.7)

        # Background hills (lighter)
        points = [(0, horizon_y - 50)]
        for x in range(0, self.width + 50, 30):
            hill_h = 30 + 25 * math.sin(x * 0.008)
            points.append((x, horizon_y - 50 - int(hill_h)))
        points.extend([(self.width, horizon_y), (0, horizon_y)])
        draw.polygon(points, fill=(120, 200, 120, 255))

        # Foreground hills (darker green)
        points = [(0, horizon_y)]
        for x in range(0, self.width + 50, 20):
            hill_h = 20 + 15 * math.sin(x * 0.012 + 1)
            points.append((x, horizon_y - int(hill_h)))
        points.extend([(self.width, horizon_y + 50), (0, horizon_y + 50)])
        draw.polygon(points, fill=(80, 180, 80, 255))

    def _draw_buildings(self, draw, frame_num):
        """Draw cute buildings"""
        color_map = {
            'red': (220, 80, 80), 'blue': (80, 150, 220),
            'yellow': (240, 220, 80), 'green': (80, 200, 120),
            'pink': (240, 150, 180), 'purple': (180, 120, 200),
        }

        for building in self.buildings:
            bx, by = building['x'], building['y']
            bw, bh = building['width'], building['height']

            if building['type'] == 'cute_house':
                color = color_map.get(building['color'], (200, 100, 100))

                # House body
                draw.rectangle([bx, by - bh, bx + bw, by], fill=color)

                # Roof
                draw.polygon([
                    (bx - 10, by - bh),
                    (bx + bw // 2, by - bh - bh // 2),
                    (bx + bw + 10, by - bh)
                ], fill=(150, 80, 60))

                # Door
                draw.rectangle([bx + bw//2 - 12, by - 40, bx + bw//2 + 12, by],
                              fill=(100, 60, 40))

                # Windows
                draw.rectangle([bx + 15, by - bh + 20, bx + 35, by - bh + 45],
                              fill=(200, 230, 255))
                draw.rectangle([bx + bw - 35, by - bh + 20, bx + bw - 15, by - bh + 45],
                              fill=(200, 230, 255))

            elif building['type'] == 'tree':
                # Trunk
                draw.rectangle([bx + bw//2 - 10, by - bh//2, bx + bw//2 + 10, by],
                              fill=(120, 80, 50))
                # Foliage
                draw.ellipse([bx, by - bh, bx + bw, by - bh//3], fill=(60, 180, 80))

            elif building['type'] == 'flower':
                color = color_map.get(building['color'], (255, 150, 150))
                # Stem
                draw.line([(bx, by), (bx, by - bh)], fill=(80, 160, 80), width=3)
                # Petals
                for i in range(5):
                    angle = i * 2 * math.pi / 5 + frame_num * 0.02
                    px = bx + int(12 * math.cos(angle))
                    py = by - bh + int(12 * math.sin(angle))
                    draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=color)
                # Center
                draw.ellipse([bx - 6, by - bh - 6, bx + 6, by - bh + 6], fill=(255, 220, 100))

    def _draw_ground(self, draw, frame_num):
        """Green grass ground"""
        horizon_y = int(self.height * 0.7)
        draw.rectangle([0, horizon_y, self.width, self.height], fill=(100, 180, 100, 255))

    def _draw_particles(self, draw, frame_num):
        """Draw butterflies"""
        color_map = {
            'pink': (255, 150, 180), 'yellow': (255, 230, 100),
            'blue': (100, 180, 255), 'purple': (200, 150, 255),
        }

        for bf in self.butterflies:
            bx = (bf['x'] + frame_num * bf['speed']) % self.width
            by = bf['y'] + math.sin(frame_num * 0.05 + bf['x'] * 0.01) * 30

            wing_flap = math.sin(frame_num * bf['wing_speed']) * 0.8
            size = bf['size']
            color = color_map.get(bf['color'], (255, 200, 200))

            # Wings
            draw.ellipse([bx - size * (1 + wing_flap), by - size//2,
                         bx - 2, by + size//2], fill=color)
            draw.ellipse([bx + 2, by - size//2,
                         bx + size * (1 + wing_flap), by + size//2], fill=color)
            # Body
            draw.ellipse([bx - 3, by - size//3, bx + 3, by + size//3], fill=(60, 40, 40))


def get_scenery_class(category: str):
    """Get appropriate scenery class for content category"""
    scenery_map = {
        'halal': AnimatedScenery,
        'islamic': AnimatedScenery,
        'horror': HorrorScenery,
        'mystery': HorrorScenery,  # Use horror style for mystery too
        'kids': KidsScenery,
        'default': AnimatedScenery,
    }
    return scenery_map.get(category, AnimatedScenery)


if __name__ == "__main__":
    # Create demo for each style
    print("Creating scenery demos...")

    # Islamic
    create_scenery_video("output/scenery_islamic.mp4", duration=6)

    # Horror
    print("\nCreating horror scenery...")
    horror = HorrorScenery(1920, 1080)
    # ... similar video creation

    # Kids
    print("\nCreating kids scenery...")
    kids = KidsScenery(1920, 1080)
    # ... similar video creation
