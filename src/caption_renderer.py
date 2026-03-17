"""
Simple Caption Renderer - Box fits exactly to text
No complex effects, just clean rendering
"""
import math
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

ASSETS_DIR = Path(__file__).parent.parent / "assets"


def get_font(size=48):
    """Get Amiri font for Arabic/Urdu"""
    font_paths = [
        str(ASSETS_DIR / "Amiri-Regular.ttf"),
        "/System/Library/Fonts/GeezaPro.ttc",
        "/System/Library/Fonts/SFArabic.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()


def draw_caption(
    img: Image.Image,
    text: str,
    font: ImageFont.FreeTypeFont,
    is_arabic: bool = False,
    frame_in_caption: int = 0,
    total_frames: int = 100,
    effect: str = "fade",
    position: str = "center",  # "center", "top", "bottom"
) -> Image.Image:
    """
    Draw caption with box that EXACTLY fits the text

    Args:
        img: RGBA image to draw on
        text: Caption text (already reshaped for RTL)
        font: Font to use
        is_arabic: Whether text is Arabic (golden color)
        frame_in_caption: Current frame within caption
        total_frames: Total frames for this caption
        effect: Animation effect (fade, none)
        position: Caption position - "center", "top", or "bottom"
    """
    if not text:
        return img

    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Calculate text dimensions
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Box padding - tight fit
    pad_x = 40
    pad_y = 25

    # Box dimensions - exactly fits text
    box_width = text_width + pad_x * 2
    box_height = text_height + pad_y * 2

    # Box position - centered horizontally, vertical based on position param
    box_x = (width - box_width) // 2
    if position == "top":
        box_y = 150
    elif position == "bottom":
        box_y = height - box_height - 80
    else:  # center - default
        box_y = (height - box_height) // 2

    # Text position - centered in box
    text_x = box_x + pad_x
    text_y = box_y + pad_y

    # Calculate alpha for fade effect
    fade_frames = 8
    if effect == "fade":
        if frame_in_caption < fade_frames:
            alpha = int(255 * frame_in_caption / fade_frames)
        elif frame_in_caption > total_frames - fade_frames:
            alpha = int(255 * (total_frames - frame_in_caption) / fade_frames)
        else:
            alpha = 255
    else:
        alpha = 255

    # Draw box background
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    box_alpha = int(230 * alpha / 255)
    overlay_draw.rounded_rectangle(
        [box_x, box_y, box_x + box_width, box_y + box_height],
        radius=15,
        fill=(0, 0, 0, box_alpha)
    )

    # Subtle border
    border_alpha = int(80 * alpha / 255)
    overlay_draw.rounded_rectangle(
        [box_x, box_y, box_x + box_width, box_y + box_height],
        radius=15,
        outline=(255, 215, 0, border_alpha),
        width=2
    )

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Text colors
    if is_arabic:
        text_color = (255, 215, 0, alpha)  # Golden
    else:
        text_color = (255, 255, 255, alpha)  # White

    shadow_alpha = int(200 * alpha / 255)
    shadow_color = (0, 0, 0, shadow_alpha)

    # Draw shadow
    draw.text((text_x + 2, text_y + 2), text, fill=shadow_color, font=font)

    # Draw main text
    draw.text((text_x, text_y), text, fill=text_color, font=font)

    return img


def draw_arabic_caption(
    img: Image.Image,
    text: str,
    font: ImageFont.FreeTypeFont,
    frame_in_caption: int = 0,
    total_frames: int = 100,
    position: str = "center",  # "center", "top", "bottom"
) -> Image.Image:
    """
    Draw Arabic caption with golden styling
    Position: center (default), top, or bottom - consistent with Urdu captions
    """
    if not text:
        return img

    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Calculate text dimensions
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Box padding
    pad_x = 50
    pad_y = 30

    # Box dimensions
    box_width = text_width + pad_x * 2
    box_height = text_height + pad_y * 2

    # Position - CENTER by default for consistency
    box_x = (width - box_width) // 2
    if position == "top":
        box_y = 150
    elif position == "bottom":
        box_y = height - box_height - 80
    else:  # center - default
        box_y = (height - box_height) // 2

    text_x = box_x + pad_x
    text_y = box_y + pad_y

    # Fade
    fade_frames = 8
    if frame_in_caption < fade_frames:
        alpha = int(255 * frame_in_caption / fade_frames)
    elif frame_in_caption > total_frames - fade_frames:
        alpha = int(255 * (total_frames - frame_in_caption) / fade_frames)
    else:
        alpha = 255

    # Draw box with elegant dark background
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    box_alpha = int(200 * alpha / 255)
    overlay_draw.rounded_rectangle(
        [box_x, box_y, box_x + box_width, box_y + box_height],
        radius=15,
        fill=(5, 10, 25, box_alpha)
    )

    # Golden border
    border_alpha = int(180 * alpha / 255)
    overlay_draw.rounded_rectangle(
        [box_x, box_y, box_x + box_width, box_y + box_height],
        radius=15,
        outline=(255, 215, 0, border_alpha),
        width=2
    )

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Golden text with shadow
    shadow_alpha = int(200 * alpha / 255)
    draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, shadow_alpha), font=font)
    draw.text((text_x, text_y), text, fill=(255, 215, 0, alpha), font=font)

    return img
