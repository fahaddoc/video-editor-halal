"""
Halal Video Generator - Web UI
A beautiful Streamlit interface for generating Islamic content videos
"""
import streamlit as st
import sys
import os
from pathlib import Path
import time

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config import OUTPUT_DIR, ASSETS_DIR
from src.script_generator import (
    get_categories,
    get_scripts_by_category,
    ISLAMIC_STORIES,
)
from src.voice_generator import generate_voice, list_available_voices
from src.stock_footage import create_fallback_backgrounds
from src.video_creator import VideoCreator, create_thumbnail

# Page config
st.set_page_config(
    page_title="Halal Video Generator",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
        color: #eee;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #0e4429;
        border-radius: 10px;
        border-left: 5px solid #2ea043;
    }
    .info-box {
        padding: 1rem;
        background-color: #1c3d5a;
        border-radius: 10px;
        border-left: 5px solid #58a6ff;
    }
    .script-preview {
        background-color: #161b22;
        padding: 1rem;
        border-radius: 10px;
        max-height: 400px;
        overflow-y: auto;
        font-family: monospace;
        white-space: pre-wrap;
    }
    .stProgress > div > div > div > div {
        background-color: #2ea043;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🌙 Halal Video Generator</div>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Create Islamic Content Videos with AI Voice</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/mosque.png", width=80)
    st.title("Settings")

    st.markdown("---")

    # Category selection
    st.subheader("📚 Content Category")
    categories = get_categories()
    category_names = list(categories.values())
    selected_category_name = st.selectbox(
        "Select Category",
        category_names,
        label_visibility="collapsed"
    )

    # Get category key
    category_key = None
    for key, name in categories.items():
        if name == selected_category_name:
            category_key = key
            break

    st.markdown("---")

    # Voice selection
    st.subheader("🎙️ Voice Settings")
    voices = list_available_voices()
    voice_names = [v[1] for v in voices.values()]
    selected_voice_name = st.selectbox(
        "Select Voice",
        voice_names,
        label_visibility="collapsed"
    )

    # Get voice key
    voice_key = "urdu_male"
    for key, (vid, vname) in voices.items():
        if vname == selected_voice_name:
            voice_key = vid
            break

    st.markdown("---")

    # Output folder
    st.subheader("📁 Output")
    if st.button("📂 Open Output Folder"):
        os.system(f'open "{OUTPUT_DIR}"')

    st.caption(f"Path: {OUTPUT_DIR}")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📜 Select Script")

    # Get scripts for selected category
    scripts = get_scripts_by_category(category_key)

    if scripts:
        script_titles = [s['title'] for s in scripts]
        selected_title = st.selectbox(
            "Choose a script",
            script_titles,
            label_visibility="collapsed"
        )

        # Find selected script
        selected_script = None
        for s in scripts:
            if s['title'] == selected_title:
                selected_script = s
                break

        if selected_script:
            st.markdown("**Preview:**")
            st.markdown(f'<div class="script-preview">{selected_script["script"][:1500]}...</div>',
                       unsafe_allow_html=True)
    else:
        st.warning("No scripts found in this category")
        selected_script = None

with col2:
    st.subheader("🎬 Generate Video")

    if selected_script:
        st.markdown(f'<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"**Title:** {selected_script['title']}")
        st.markdown(f"**Category:** {selected_category_name}")
        st.markdown(f"**Voice:** {selected_voice_name}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("")

        # Generate button
        if st.button("🚀 Generate Video", type="primary", use_container_width=True):

            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # Step 1: Generate voice
                status_text.text("🎙️ Generating voiceover...")
                progress_bar.progress(10)

                safe_title = selected_script['title'].lower().replace(" ", "_").replace(".", "")
                audio_path = OUTPUT_DIR / f"{safe_title}.mp3"

                generate_voice(
                    selected_script['script'],
                    output_path=audio_path,
                    voice=voice_key
                )
                progress_bar.progress(40)

                # Step 2: Create backgrounds
                status_text.text("🎨 Creating backgrounds...")
                backgrounds = create_fallback_backgrounds(ASSETS_DIR, 5)
                progress_bar.progress(50)

                # Step 3: Create video
                status_text.text("🎬 Creating video (this may take a minute)...")
                video_path = OUTPUT_DIR / f"{safe_title}.mp4"

                creator = VideoCreator()
                creator.create_video_from_audio_and_images(
                    audio_path=audio_path,
                    image_paths=backgrounds,
                    output_path=video_path,
                )
                progress_bar.progress(85)

                # Step 4: Create thumbnail
                status_text.text("🖼️ Creating thumbnail...")
                thumb_path = OUTPUT_DIR / f"{safe_title}_thumb.png"
                create_thumbnail(selected_script['title'], thumb_path)
                progress_bar.progress(100)

                status_text.text("✅ Complete!")

                # Success message
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("Video generated successfully!")
                st.markdown('</div>', unsafe_allow_html=True)

                # Store paths in session state
                st.session_state['last_video'] = str(video_path)
                st.session_state['last_audio'] = str(audio_path)
                st.session_state['last_thumb'] = str(thumb_path)

            except Exception as e:
                st.error(f"Error: {str(e)}")
                progress_bar.progress(0)

# Video Preview Section
st.markdown("---")
st.subheader("📺 Video Preview")

if 'last_video' in st.session_state and os.path.exists(st.session_state['last_video']):
    video_path = st.session_state['last_video']
    audio_path = st.session_state.get('last_audio', '')
    thumb_path = st.session_state.get('last_thumb', '')

    col_vid, col_info = st.columns([2, 1])

    with col_vid:
        st.video(video_path)

    with col_info:
        st.markdown("**Generated Files:**")

        # Video info
        if os.path.exists(video_path):
            video_size = os.path.getsize(video_path) / (1024*1024)
            st.markdown(f"🎬 Video: `{os.path.basename(video_path)}`")
            st.markdown(f"   Size: {video_size:.1f} MB")

        # Audio info
        if audio_path and os.path.exists(audio_path):
            audio_size = os.path.getsize(audio_path) / (1024*1024)
            st.markdown(f"🎙️ Audio: `{os.path.basename(audio_path)}`")
            st.markdown(f"   Size: {audio_size:.1f} MB")

        # Thumbnail
        if thumb_path and os.path.exists(thumb_path):
            st.markdown(f"🖼️ Thumbnail: `{os.path.basename(thumb_path)}`")
            st.image(thumb_path, width=200)

        st.markdown("---")

        # Download buttons
        with open(video_path, 'rb') as f:
            st.download_button(
                "⬇️ Download Video",
                f,
                file_name=os.path.basename(video_path),
                mime="video/mp4",
                use_container_width=True
            )
else:
    st.info("👆 Generate a video to preview it here")

# Previously generated videos
st.markdown("---")
st.subheader("📁 Previously Generated Videos")

video_files = list(OUTPUT_DIR.glob("*.mp4"))
if video_files:
    cols = st.columns(3)
    for idx, video_file in enumerate(sorted(video_files, key=os.path.getmtime, reverse=True)[:6]):
        with cols[idx % 3]:
            st.markdown(f"**{video_file.stem}**")

            # Check for thumbnail
            thumb_file = OUTPUT_DIR / f"{video_file.stem}_thumb.png"
            if thumb_file.exists():
                st.image(str(thumb_file), use_container_width=True)

            if st.button(f"▶️ Preview", key=f"preview_{idx}"):
                st.session_state['last_video'] = str(video_file)
                st.session_state['last_audio'] = str(OUTPUT_DIR / f"{video_file.stem}.mp3")
                st.session_state['last_thumb'] = str(thumb_file)
                st.rerun()
else:
    st.info("No videos generated yet. Create your first video above!")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>🌙 Halal Video Generator | Made for Islamic Content Creators</p>",
    unsafe_allow_html=True
)
