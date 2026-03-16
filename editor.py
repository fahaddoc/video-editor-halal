"""
Halal Video Editor - Full Featured Video Editor
Professional Islamic content video creator
"""
import streamlit as st
import sys
import os
import json
from pathlib import Path
import time

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config import OUTPUT_DIR, ASSETS_DIR

# Page config
st.set_page_config(
    page_title="Halal Video Editor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #eee;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .arabic-text {
        font-family: 'Amiri', serif;
        font-size: 1.8rem;
        text-align: center;
        color: #ffd700;
        direction: rtl;
        padding: 1rem;
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
        margin: 1rem 0;
    }

    .urdu-text {
        font-family: 'Amiri', serif;
        font-size: 1.3rem;
        text-align: right;
        direction: rtl;
        line-height: 2;
        padding: 1rem;
        background: rgba(30,40,60,0.5);
        border-radius: 10px;
    }

    .preview-box {
        background: linear-gradient(180deg, #0a0a15 0%, #1a1a2e 100%);
        border-radius: 15px;
        padding: 20px;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
    }

    .caption-preview {
        font-family: 'Amiri', serif;
        font-size: 1.5rem;
        color: white;
        text-align: center;
        padding: 15px 30px;
        background: rgba(0,0,0,0.7);
        border-radius: 10px;
        direction: rtl;
        max-width: 80%;
    }

    .tab-content {
        padding: 1.5rem;
        background: rgba(20,25,35,0.5);
        border-radius: 10px;
        margin-top: 1rem;
    }

    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 5px;
    }

    .badge-verified {
        background: #1e5631;
        color: #90EE90;
    }

    .badge-pending {
        background: #5c4033;
        color: #FFD700;
    }

    .timeline-bar {
        height: 60px;
        background: #1a1a2e;
        border-radius: 10px;
        margin: 10px 0;
        position: relative;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a2e;
        border-radius: 10px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'project' not in st.session_state:
    st.session_state.project = {
        'title': '',
        'title_urdu': '',
        'arabic_text': '',
        'arabic_verified': False,
        'arabic_source': '',
        'script_urdu': '',
        'captions': [],
        'voice': 'ur-PK-AsadNeural',
        'voice_speed': '-5%',
        'bg_type': 'nature',
        'bg_videos': [],
        'text_style': 'centered',
        'text_animation': 'fade',
        'audio_path': None,
        'video_path': None,
    }

# Header
st.markdown('<div class="main-header">🎬 Halal Video Editor</div>', unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Content",
    "🎙️ Audio",
    "🎨 Visuals",
    "⏱️ Timeline",
    "📤 Export"
])

# ==================== TAB 1: CONTENT ====================
with tab1:
    st.subheader("📝 Content & Script")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Video Title")
        st.session_state.project['title'] = st.text_input(
            "English/Roman Title",
            value=st.session_state.project.get('title', ''),
            placeholder="e.g., The Power of Smiling"
        )

        st.session_state.project['title_urdu'] = st.text_input(
            "عنوان (Urdu Title)",
            value=st.session_state.project.get('title_urdu', ''),
            placeholder="مثال: مسکرانے کی طاقت"
        )

        st.markdown("---")

        st.markdown("### Arabic Text (Hadith/Ayat)")
        st.warning("⚠️ Only add verified Arabic text from authentic sources!")

        st.session_state.project['arabic_text'] = st.text_area(
            "Arabic Text (اردو)",
            value=st.session_state.project.get('arabic_text', ''),
            placeholder="تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ",
            height=80
        )

        st.session_state.project['arabic_source'] = st.text_input(
            "Source/Reference",
            value=st.session_state.project.get('arabic_source', ''),
            placeholder="e.g., Sahih al-Bukhari 6021, Sunan al-Tirmidhi 1956"
        )

        st.session_state.project['arabic_verified'] = st.checkbox(
            "✅ I have verified this text from authentic sources",
            value=st.session_state.project.get('arabic_verified', False)
        )

        if st.session_state.project['arabic_verified']:
            st.success("Verified ✓")
        else:
            st.info("Please verify before using")

    with col2:
        st.markdown("### Script (Urdu)")
        st.markdown("*Write in Urdu script for best voice quality*")

        st.session_state.project['script_urdu'] = st.text_area(
            "اسکرپٹ",
            value=st.session_state.project.get('script_urdu', ''),
            height=300,
            placeholder="""رسول اللہ صلی اللہ علیہ وسلم نے فرمایا:
اپنے بھائی کے سامنے مسکرانا صدقہ ہے۔

آج ہم اس خوبصورت حدیث کو سمجھیں گے..."""
        )

        # Preview
        if st.session_state.project['script_urdu']:
            st.markdown("**Preview:**")
            st.markdown(
                f'<div class="urdu-text">{st.session_state.project["script_urdu"][:500]}...</div>',
                unsafe_allow_html=True
            )

    # Captions editor
    st.markdown("---")
    st.markdown("### 📜 Captions/Subtitles")
    st.info("Add captions that will appear in the video. These will animate like TikTok/Reels.")

    # Auto-generate captions from script
    if st.button("🔄 Auto-generate from Script"):
        if st.session_state.project['script_urdu']:
            lines = [l.strip() for l in st.session_state.project['script_urdu'].split('\n') if l.strip()]
            st.session_state.project['captions'] = lines
            st.success(f"Generated {len(lines)} captions!")
            st.rerun()

    # Display captions
    captions = st.session_state.project.get('captions', [])
    if captions:
        st.markdown(f"**{len(captions)} Captions:**")
        for i, cap in enumerate(captions[:10]):
            col_num, col_text, col_del = st.columns([0.5, 5, 0.5])
            with col_num:
                st.write(f"{i+1}.")
            with col_text:
                st.markdown(f'<div style="direction:rtl; text-align:right;">{cap}</div>',
                           unsafe_allow_html=True)
        if len(captions) > 10:
            st.caption(f"... and {len(captions) - 10} more")


# ==================== TAB 2: AUDIO ====================
with tab2:
    st.subheader("🎙️ Audio Settings")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Voice Selection")

        voice_options = {
            "Urdu - Male (Asad)": "ur-PK-AsadNeural",
            "Urdu - Female (Uzma)": "ur-PK-UzmaNeural",
            "Arabic - Male (Hamed)": "ar-SA-HamedNeural",
            "Arabic - Female (Zariyah)": "ar-SA-ZariyahNeural",
            "Hindi - Male (Madhur)": "hi-IN-MadhurNeural",
            "Hindi - Female (Swara)": "hi-IN-SwaraNeural",
        }

        selected_voice = st.selectbox(
            "Select Voice",
            list(voice_options.keys()),
            index=0
        )
        st.session_state.project['voice'] = voice_options[selected_voice]

        st.markdown("### Voice Settings")

        speed = st.slider("Speed", min_value=-30, max_value=30, value=-5, step=5)
        st.session_state.project['voice_speed'] = f"{speed:+d}%"

        st.markdown("---")

        st.markdown("### Or Upload Your Own Audio")
        uploaded_audio = st.file_uploader(
            "Upload MP3/WAV",
            type=['mp3', 'wav'],
            help="Upload your own voiceover"
        )

        if uploaded_audio:
            audio_path = OUTPUT_DIR / f"uploaded_{uploaded_audio.name}"
            with open(audio_path, 'wb') as f:
                f.write(uploaded_audio.read())
            st.session_state.project['audio_path'] = str(audio_path)
            st.success(f"Uploaded: {uploaded_audio.name}")

    with col2:
        st.markdown("### Audio Preview")

        if st.button("🎵 Generate Voice Preview", type="primary"):
            if st.session_state.project['script_urdu']:
                with st.spinner("Generating voice..."):
                    try:
                        import asyncio
                        import edge_tts

                        preview_text = st.session_state.project['script_urdu'][:500]
                        preview_path = OUTPUT_DIR / "voice_preview.mp3"

                        async def gen_preview():
                            communicate = edge_tts.Communicate(
                                text=preview_text,
                                voice=st.session_state.project['voice'],
                                rate=st.session_state.project['voice_speed']
                            )
                            await communicate.save(str(preview_path))

                        asyncio.run(gen_preview())
                        st.session_state.project['audio_path'] = str(preview_path)
                        st.success("Voice generated!")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please add script first!")

        # Audio player
        audio_path = st.session_state.project.get('audio_path')
        if audio_path and os.path.exists(audio_path):
            st.audio(audio_path)
            st.caption(f"File: {os.path.basename(audio_path)}")


# ==================== TAB 3: VISUALS ====================
with tab3:
    st.subheader("🎨 Visual Settings")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Background Type")

        bg_type = st.radio(
            "Select Background",
            ["🌿 Nature Videos", "🌙 Animated (Stars/Moon)", "🎨 Solid Color", "📤 Upload Custom"],
            index=0
        )

        if "Nature" in bg_type:
            st.session_state.project['bg_type'] = 'nature'
            st.markdown("**Nature Video Categories:**")

            nature_cats = st.multiselect(
                "Select categories",
                ["Clouds/Sky", "Mountains", "Ocean/Water", "Forest", "Sunset/Sunrise", "Rain", "Stars/Night"],
                default=["Clouds/Sky", "Sunset/Sunrise"]
            )

            st.info("💡 Nature videos will be downloaded from Pexels (free)")

            pexels_key = st.text_input(
                "Pexels API Key (optional)",
                type="password",
                help="Get free key from pexels.com/api"
            )

        elif "Animated" in bg_type:
            st.session_state.project['bg_type'] = 'animated'
            anim_style = st.selectbox(
                "Animation Style",
                ["Starfield with Moon", "Floating Particles", "Geometric Patterns", "Gradient Waves"]
            )

        elif "Solid" in bg_type:
            st.session_state.project['bg_type'] = 'solid'
            bg_color = st.color_picker("Background Color", "#1a1a2e")

        else:
            st.session_state.project['bg_type'] = 'custom'
            uploaded_bg = st.file_uploader("Upload Video/Image", type=['mp4', 'mov', 'jpg', 'png'])

        st.markdown("---")

        st.markdown("### Background Settings")
        bg_dim = st.slider("Dim Background", 0, 100, 40, help="Darken background for text visibility")

    with col2:
        st.markdown("### Text Style")

        text_position = st.selectbox(
            "Caption Position",
            ["Center (TikTok style)", "Bottom", "Top"],
            index=0
        )
        st.session_state.project['text_style'] = text_position.lower().split()[0]

        text_animation = st.selectbox(
            "Caption Animation",
            ["Word-by-word (Karaoke)", "Fade In/Out", "Slide Up", "Typewriter", "Pop/Scale"],
            index=0
        )
        st.session_state.project['text_animation'] = text_animation.lower().split()[0]

        st.markdown("### Text Appearance")

        col_font, col_size = st.columns(2)
        with col_font:
            font_style = st.selectbox("Font", ["Amiri (Arabic)", "Noto Nastaliq", "Arial"])
        with col_size:
            font_size = st.slider("Size", 24, 72, 42)

        text_color = st.color_picker("Text Color", "#FFFFFF")

        show_text_bg = st.checkbox("Show text background", value=True)
        if show_text_bg:
            text_bg_opacity = st.slider("Background opacity", 0, 100, 70)

        st.markdown("---")

        st.markdown("### Preview")
        st.markdown("""
        <div class="preview-box">
            <div style="color: #ffd700; font-family: 'Amiri', serif; font-size: 1.5rem; margin-bottom: 20px; direction: rtl;">
                تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ
            </div>
            <div class="caption-preview">
                مسکرانا صدقہ ہے
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==================== TAB 4: TIMELINE ====================
with tab4:
    st.subheader("⏱️ Timeline & Sync")

    st.info("Timeline editor - sync captions with audio, adjust timing")

    # Audio waveform placeholder
    st.markdown("### Audio Timeline")
    st.markdown("""
    <div class="timeline-bar">
        <div style="position:absolute; left:0; top:0; bottom:0; width:30%; background: linear-gradient(90deg, #4CAF50, #2196F3); opacity:0.7;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Captions timeline
    st.markdown("### Captions Timeline")

    captions = st.session_state.project.get('captions', [])
    if captions:
        for i, cap in enumerate(captions[:5]):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.text(f"{i+1}. {cap[:40]}...")
            with col2:
                st.number_input(f"Start {i}", value=i*3.0, key=f"start_{i}", label_visibility="collapsed")
            with col3:
                st.number_input(f"End {i}", value=(i+1)*3.0, key=f"end_{i}", label_visibility="collapsed")
    else:
        st.warning("No captions added yet. Go to Content tab to add captions.")

    st.markdown("---")

    # Preview
    st.markdown("### Video Preview")
    if st.button("▶️ Generate Preview (30 sec)", type="primary"):
        st.info("Preview generation will be implemented...")


# ==================== TAB 5: EXPORT ====================
with tab5:
    st.subheader("📤 Export Video")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Export Settings")

        resolution = st.selectbox(
            "Resolution",
            ["1080p (1920x1080) - YouTube", "720p (1280x720)", "1080x1920 - TikTok/Reels"],
            index=0
        )

        quality = st.selectbox(
            "Quality",
            ["High (larger file)", "Medium (balanced)", "Low (smaller file)"],
            index=1
        )

        st.markdown("---")

        st.markdown("### Project Summary")

        project = st.session_state.project

        checks = {
            "Title": bool(project.get('title') or project.get('title_urdu')),
            "Script": bool(project.get('script_urdu')),
            "Arabic (verified)": project.get('arabic_verified', False),
            "Audio": bool(project.get('audio_path')),
            "Captions": len(project.get('captions', [])) > 0,
        }

        for item, status in checks.items():
            if status:
                st.markdown(f"✅ {item}")
            else:
                st.markdown(f"⬜ {item}")

        ready = all(checks.values())

    with col2:
        st.markdown("### Generate Video")

        if ready:
            if st.button("🎬 Generate Final Video", type="primary", use_container_width=True):
                with st.spinner("Generating video... This may take a few minutes."):
                    progress = st.progress(0)
                    status = st.empty()

                    status.text("Preparing assets...")
                    progress.progress(10)
                    time.sleep(1)

                    status.text("Creating backgrounds...")
                    progress.progress(30)
                    time.sleep(1)

                    status.text("Rendering frames...")
                    progress.progress(60)
                    time.sleep(1)

                    status.text("Adding audio...")
                    progress.progress(80)
                    time.sleep(1)

                    status.text("Finalizing...")
                    progress.progress(100)

                    st.success("Video generated! (Demo mode)")
        else:
            st.warning("Please complete all required fields before exporting.")
            st.markdown("**Missing:**")
            for item, status in checks.items():
                if not status:
                    st.markdown(f"- {item}")

    st.markdown("---")

    # Previous exports
    st.markdown("### Previous Exports")

    video_files = list(OUTPUT_DIR.glob("*.mp4"))
    if video_files:
        for vf in sorted(video_files, key=os.path.getmtime, reverse=True)[:3]:
            col_name, col_size, col_btn = st.columns([3, 1, 1])
            with col_name:
                st.text(vf.name)
            with col_size:
                size = os.path.getsize(vf) / (1024*1024)
                st.text(f"{size:.1f} MB")
            with col_btn:
                if st.button("▶️", key=f"play_{vf.name}"):
                    st.video(str(vf))


# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### 🎬 Project")

    # Save/Load project
    if st.button("💾 Save Project"):
        project_path = OUTPUT_DIR / "project.json"
        with open(project_path, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.project, f, ensure_ascii=False, indent=2)
        st.success("Project saved!")

    if st.button("📂 Load Project"):
        project_path = OUTPUT_DIR / "project.json"
        if project_path.exists():
            with open(project_path, 'r', encoding='utf-8') as f:
                st.session_state.project = json.load(f)
            st.success("Project loaded!")
            st.rerun()

    st.markdown("---")

    st.markdown("### 📚 Templates")

    template = st.selectbox(
        "Quick Start",
        ["-- Select --", "Hadith Video", "Quran Ayat", "Islamic Story", "Motivational"]
    )

    if template != "-- Select --":
        if st.button("Load Template"):
            st.info(f"Loading {template} template...")

    st.markdown("---")

    st.markdown("### ℹ️ Help")
    st.markdown("""
    1. Add content in **Content** tab
    2. Generate/upload audio in **Audio** tab
    3. Customize visuals in **Visuals** tab
    4. Sync timing in **Timeline** tab
    5. Export final video in **Export** tab
    """)

    st.markdown("---")

    if st.button("📁 Open Output Folder"):
        os.system(f'open "{OUTPUT_DIR}"')


# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>🌙 Halal Video Editor | Professional Islamic Content Creator</p>",
    unsafe_allow_html=True
)
