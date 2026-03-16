"""
Simple Halal Video Generator - Working Version
"""
import streamlit as st
import os
import sys
import asyncio
import nest_asyncio
from pathlib import Path

# Fix asyncio for Streamlit
nest_asyncio.apply()

sys.path.insert(0, str(Path(__file__).parent))
from config import OUTPUT_DIR, ASSETS_DIR

st.set_page_config(page_title="Halal Video Generator", page_icon="🕌", layout="wide")

# Simple CSS
st.markdown("""
<style>
    .main-title { text-align: center; color: #ffd700; font-size: 2.5rem; padding: 1rem; }
    .urdu-box { direction: rtl; text-align: right; font-size: 1.2rem; padding: 1rem;
                background: #1a1a2e; border-radius: 10px; line-height: 2; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🕌 Halal Video Generator</h1>', unsafe_allow_html=True)

# Templates
TEMPLATES = {
    "مسکرانے کی طاقت": {
        "title_urdu": "مسکرانے کی طاقت",
        "arabic": "تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ",
        "script": """رسول اللہ صلی اللہ علیہ وسلم نے فرمایا:
اپنے بھائی کے سامنے مسکرانا صدقہ ہے۔
یہ حدیث جامع ترمذی میں ہے۔
مسکرانا بھی صدقہ ہے۔
اچھی بات کہنا بھی صدقہ ہے۔
سبسکرائب کریں۔
اللہ حافظ۔"""
    },
    "صبر کا اجر": {
        "title_urdu": "صبر کا اجر",
        "arabic": "إِنَّمَا يُوَفَّى الصَّابِرُونَ أَجْرَهُم بِغَيْرِ حِسَابٍ",
        "script": """اللہ تعالیٰ فرماتے ہیں:
صبر کرنے والوں کو بے حساب اجر ملے گا۔
صبر کا مطلب ہے مشکل میں ثابت قدم رہنا۔
اللہ صبر کرنے والوں کے ساتھ ہے۔
سبسکرائب کریں۔
اللہ حافظ۔"""
    },
    "دعا کی طاقت": {
        "title_urdu": "دعا کی طاقت",
        "arabic": "ادْعُونِي أَسْتَجِبْ لَكُمْ",
        "script": """اللہ تعالیٰ فرماتے ہیں:
مجھ سے دعا کرو، میں قبول کروں گا۔
دعا مومن کا ہتھیار ہے۔
اللہ سنتے ہیں، اللہ قریب ہیں۔
سبسکرائب کریں۔
اللہ حافظ۔"""
    },
}

# Sidebar - Template Selection
st.sidebar.header("📚 Templates")
selected_template = st.sidebar.selectbox("Select Template", list(TEMPLATES.keys()))

if st.sidebar.button("📥 Load Template", use_container_width=True):
    st.session_state.template = TEMPLATES[selected_template]
    st.sidebar.success("✅ Loaded!")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Content")

    # Get template data
    template = st.session_state.get('template', TEMPLATES[selected_template])

    title = st.text_input("Title (Urdu)", value=template.get('title_urdu', ''))
    arabic = st.text_input("Arabic Text", value=template.get('arabic', ''))
    script = st.text_area("Script (Urdu)", value=template.get('script', ''), height=250)

    st.markdown(f'<div class="urdu-box">{script}</div>', unsafe_allow_html=True)

with col2:
    st.subheader("🎬 Generate")

    voice = st.selectbox("Voice", ["Urdu Male", "Urdu Female", "Arabic Male"])
    voice_map = {
        "Urdu Male": "ur-PK-AsadNeural",
        "Urdu Female": "ur-PK-UzmaNeural",
        "Arabic Male": "ar-SA-HamedNeural"
    }

    st.markdown("---")

    if st.button("🚀 GENERATE VIDEO", type="primary", use_container_width=True):
        if not script.strip():
            st.error("Please add script first!")
        else:
            progress = st.progress(0)
            status = st.empty()

            try:
                import edge_tts
                import subprocess
                import math
                import numpy as np
                from PIL import Image, ImageDraw, ImageFont
                import datetime

                timestamp = datetime.datetime.now().strftime("%H%M%S")
                audio_path = OUTPUT_DIR / f"audio_{timestamp}.mp3"
                video_path = OUTPUT_DIR / f"video_{timestamp}.mp4"
                frames_dir = ASSETS_DIR / "frames"
                frames_dir.mkdir(exist_ok=True)

                # Clean frames
                for f in frames_dir.glob("*.png"):
                    f.unlink()

                # Step 1: Audio
                status.text("🎙️ Generating voice...")
                progress.progress(10)

                async def gen_audio():
                    comm = edge_tts.Communicate(script, voice_map[voice], rate="-5%")
                    await comm.save(str(audio_path))
                asyncio.run(gen_audio())

                progress.progress(25)
                status.text("📏 Getting duration...")

                # Get duration
                result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
                    capture_output=True, text=True
                )
                duration = float(result.stdout.strip())

                # Step 2: Frames
                fps = 24
                total_frames = int(duration * fps)
                width, height = 1920, 1080

                captions = [l.strip() for l in script.split('\n') if l.strip()]
                frames_per_cap = total_frames // max(len(captions), 1)

                # Font
                font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, 44)
                    title_font = ImageFont.truetype(font_path, 55)
                else:
                    font = ImageFont.load_default()
                    title_font = font

                # Stars
                np.random.seed(42)
                stars = [{'x': np.random.randint(0,width), 'y': np.random.randint(0,height),
                         's': np.random.randint(1,4), 'b': np.random.randint(150,255)}
                        for _ in range(100)]

                status.text(f"🎨 Rendering {total_frames} frames...")

                for fn in range(total_frames):
                    img = Image.new('RGB', (width, height))
                    draw = ImageDraw.Draw(img)

                    # Background
                    for y in range(height):
                        r = int(8 + 15*y/height)
                        g = int(12 + 20*y/height)
                        b = int(25 + 40*y/height)
                        draw.line([(0,y), (width,y)], fill=(r,g,b))

                    # Stars
                    for star in stars:
                        br = star['b'] + int(20*math.sin(fn*0.06))
                        br = max(80, min(255, br))
                        x, y = star['x'], (star['y'] + fn*0.5) % height
                        draw.ellipse([x-star['s'], y-star['s'], x+star['s'], y+star['s']],
                                    fill=(br,br,int(br*0.9)))

                    # Moon
                    mx, my = width-140, 100
                    draw.ellipse([mx-40,my-40,mx+40,my+40], fill=(255,250,220))
                    draw.ellipse([mx-15,my-45,mx+55,my+45], fill=(15,22,45))

                    # Title
                    if fn < fps*5 and title:
                        try:
                            bbox = draw.textbbox((0,0), title, font=title_font)
                            x = (width - (bbox[2]-bbox[0])) // 2
                            draw.text((x+2,82), title, fill=(0,0,0), font=title_font)
                            draw.text((x,80), title, fill=(255,255,255), font=title_font)
                        except: pass

                    # Arabic
                    if fn < fps*7 and arabic:
                        try:
                            bbox = draw.textbbox((0,0), arabic, font=font)
                            x = (width - (bbox[2]-bbox[0])) // 2
                            draw.text((x,170), arabic, fill=(255,215,0), font=font)
                        except: pass

                    # Caption
                    if captions:
                        idx = min(fn // frames_per_cap, len(captions)-1)
                        cap = captions[idx]
                        try:
                            bbox = draw.textbbox((0,0), cap, font=font)
                            tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
                            x, y = (width-tw)//2, height-160
                            draw.rectangle([x-15, y-10, x+tw+15, y+th+10], fill=(0,0,0))
                            draw.text((x,y), cap, fill=(255,255,255), font=font)
                        except: pass

                    img.save(frames_dir / f"f_{fn:05d}.png")

                    if fn % 50 == 0:
                        pct = 25 + int(50 * fn / total_frames)
                        progress.progress(pct)
                        status.text(f"🎨 Frame {fn}/{total_frames}")

                # Step 3: Compile
                status.text("🎬 Compiling video...")
                progress.progress(80)

                temp_vid = OUTPUT_DIR / "temp.mp4"
                subprocess.run([
                    "ffmpeg", "-y", "-framerate", str(fps),
                    "-i", str(frames_dir / "f_%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    str(temp_vid)
                ], capture_output=True)

                # Add audio
                status.text("🔊 Adding audio...")
                progress.progress(90)

                subprocess.run([
                    "ffmpeg", "-y",
                    "-i", str(temp_vid), "-i", str(audio_path),
                    "-c:v", "copy", "-c:a", "aac", "-shortest",
                    str(video_path)
                ], capture_output=True)

                # Cleanup
                for f in frames_dir.glob("*.png"):
                    f.unlink()
                if temp_vid.exists():
                    temp_vid.unlink()

                progress.progress(100)
                status.text("✅ Done!")

                st.success("🎉 Video Generated!")
                st.video(str(video_path))

                with open(video_path, 'rb') as f:
                    st.download_button("⬇️ Download", f, file_name=video_path.name,
                                      mime="video/mp4", use_container_width=True)

                size = os.path.getsize(video_path) / (1024*1024)
                st.caption(f"📁 {video_path.name} ({size:.1f} MB)")

            except Exception as e:
                st.error(f"Error: {e}")
                import traceback
                st.code(traceback.format_exc())

# Show previous videos
st.markdown("---")
st.subheader("📂 Previous Videos")
videos = sorted(OUTPUT_DIR.glob("video_*.mp4"), key=os.path.getmtime, reverse=True)[:3]
if videos:
    for v in videos:
        col1, col2 = st.columns([4,1])
        col1.text(v.name)
        if col2.button("▶️", key=v.name):
            st.video(str(v))
else:
    st.info("No videos yet")
