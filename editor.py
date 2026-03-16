"""
Halal Video Editor - Professional Islamic Video Creator
Beautiful UI with auto-generated content and templates
"""
import streamlit as st
import sys
import os
import json
from pathlib import Path
import time
import asyncio

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config import OUTPUT_DIR, ASSETS_DIR

# Page config
st.set_page_config(
    page_title="Halal Video Editor",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== PRE-BUILT TEMPLATES ==============
TEMPLATES = {
    "hadith_smile": {
        "title": "The Power of Smiling",
        "title_urdu": "مسکرانے کی طاقت",
        "arabic_text": "تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ",
        "arabic_source": "Jami` at-Tirmidhi 1956",
        "arabic_verified": True,
        "script_urdu": """رسول اللہ صلی اللہ علیہ وسلم نے فرمایا:
اپنے بھائی کے سامنے مسکرانا صدقہ ہے۔

آج ہم اس خوبصورت حدیث کو سمجھیں گے۔

یہ حدیث جامع ترمذی میں ہے۔
کتنی سادہ بات ہے، مسکرانا صدقہ ہے۔
لیکن اس میں کتنی گہرائی ہے؟

صدقہ کا مطلب ہے وہ چیز جو اللہ کی رضا کے لیے دی جائے۔
ہم سوچتے ہیں صدقہ صرف پیسہ ہے۔

لیکن نبی صلی اللہ علیہ وسلم نے بتایا:
مسکرانا بھی صدقہ ہے۔
اچھی بات کہنا بھی صدقہ ہے۔
راستہ بتانا بھی صدقہ ہے۔

آپ جب مسکراتے ہیں تو کیا ہوتا ہے؟
سامنے والے کو اچھا لگتا ہے۔
ماحول خوشگوار ہو جاتا ہے۔

صحابہ فرماتے ہیں:
رسول اللہ صلی اللہ علیہ وسلم کا چہرہ ہمیشہ مسکراتا رہتا تھا۔

یہ تھی سنت۔

آج سے یہ کریں:
صبح آئینے میں خود کو دیکھ کر مسکرائیں۔
گھر والوں سے مسکرا کر ملیں۔

مسکرانا مت چھوڑیں۔
یہ سنت بھی ہے، ثواب بھی ہے۔

سبسکرائب کریں۔
اللہ حافظ۔""",
        "captions": [
            "رسول اللہ ﷺ نے فرمایا",
            "اپنے بھائی کے سامنے مسکرانا صدقہ ہے",
            "آج ہم اس خوبصورت حدیث کو سمجھیں گے",
            "یہ حدیث جامع ترمذی میں ہے",
            "کتنی سادہ بات ہے - مسکرانا صدقہ ہے",
            "صدقہ کا مطلب ہے وہ چیز جو اللہ کی رضا کے لیے دی جائے",
            "ہم سوچتے ہیں صدقہ صرف پیسہ ہے",
            "لیکن نبی ﷺ نے بتایا",
            "مسکرانا بھی صدقہ ہے",
            "اچھی بات کہنا بھی صدقہ ہے",
            "راستہ بتانا بھی صدقہ ہے",
            "صحابہ فرماتے ہیں",
            "رسول اللہ ﷺ کا چہرہ ہمیشہ مسکراتا رہتا تھا",
            "یہ تھی سنت",
            "آج سے یہ کریں",
            "مسکرانا مت چھوڑیں",
            "سبسکرائب کریں",
            "اللہ حافظ",
        ],
        "category": "Hadith"
    },
    "sabr_patience": {
        "title": "The Reward of Patience",
        "title_urdu": "صبر کا اجر",
        "arabic_text": "إِنَّمَا يُوَفَّى الصَّابِرُونَ أَجْرَهُم بِغَيْرِ حِسَابٍ",
        "arabic_source": "Surah Az-Zumar 39:10",
        "arabic_verified": True,
        "script_urdu": """اللہ تعالیٰ قرآن مجید میں فرماتے ہیں:
صبر کرنے والوں کو ان کا اجر بے حساب دیا جائے گا۔

سبحان اللہ! بے حساب اجر۔

آج ہم صبر کی فضیلت سمجھیں گے۔

صبر کیا ہے؟
صبر کا مطلب ہے مشکل میں ثابت قدم رہنا۔
اللہ کی رضا پر راضی رہنا۔

زندگی میں مشکلیں آتی ہیں۔
پریشانیاں آتی ہیں۔
غم آتے ہیں۔

لیکن جو صبر کرتا ہے،
اللہ اسے بے حساب اجر دیتے ہیں۔

نبی صلی اللہ علیہ وسلم نے فرمایا:
صبر روشنی ہے۔

جب مشکل آئے تو کہیں:
إِنَّا لِلَّهِ وَإِنَّا إِلَيْهِ رَاجِعُونَ

اللہ صبر کرنے والوں کے ساتھ ہے۔

سبسکرائب کریں۔
اللہ حافظ۔""",
        "captions": [
            "اللہ تعالیٰ قرآن میں فرماتے ہیں",
            "صبر کرنے والوں کو بے حساب اجر ملے گا",
            "سبحان اللہ! بے حساب اجر",
            "صبر کیا ہے؟",
            "مشکل میں ثابت قدم رہنا",
            "اللہ کی رضا پر راضی رہنا",
            "زندگی میں مشکلیں آتی ہیں",
            "لیکن جو صبر کرتا ہے",
            "اللہ اسے بے حساب اجر دیتے ہیں",
            "نبی ﷺ نے فرمایا: صبر روشنی ہے",
            "إِنَّا لِلَّهِ وَإِنَّا إِلَيْهِ رَاجِعُونَ",
            "اللہ صبر کرنے والوں کے ساتھ ہے",
            "سبسکرائب کریں",
            "اللہ حافظ",
        ],
        "category": "Quran"
    },
    "dua_importance": {
        "title": "The Power of Dua",
        "title_urdu": "دعا کی طاقت",
        "arabic_text": "ادْعُونِي أَسْتَجِبْ لَكُمْ",
        "arabic_source": "Surah Ghafir 40:60",
        "arabic_verified": True,
        "script_urdu": """اللہ تعالیٰ فرماتے ہیں:
مجھ سے دعا کرو، میں قبول کروں گا۔

کتنا بڑا وعدہ ہے اللہ کا!

دعا مومن کا ہتھیار ہے۔
دعا عبادت کا مغز ہے۔

جب کوئی راستہ نظر نہ آئے،
دعا کریں۔

جب مشکلیں گھیر لیں،
دعا کریں۔

جب دل ٹوٹ جائے،
دعا کریں۔

اللہ سنتے ہیں۔
اللہ قریب ہیں۔
اللہ جواب دیتے ہیں۔

نبی صلی اللہ علیہ وسلم نے فرمایا:
دعا عبادت ہے۔

رات کے آخری پہر میں دعا کریں۔
سجدے میں دعا کریں۔
ہر وقت اللہ سے مانگیں۔

اللہ دینے والا ہے۔
اللہ سننے والا ہے۔

سبسکرائب کریں۔
اللہ حافظ۔""",
        "captions": [
            "اللہ تعالیٰ فرماتے ہیں",
            "مجھ سے دعا کرو، میں قبول کروں گا",
            "کتنا بڑا وعدہ ہے اللہ کا!",
            "دعا مومن کا ہتھیار ہے",
            "دعا عبادت کا مغز ہے",
            "جب کوئی راستہ نظر نہ آئے، دعا کریں",
            "جب مشکلیں گھیر لیں، دعا کریں",
            "جب دل ٹوٹ جائے، دعا کریں",
            "اللہ سنتے ہیں، اللہ قریب ہیں",
            "نبی ﷺ نے فرمایا: دعا عبادت ہے",
            "رات کے آخری پہر میں دعا کریں",
            "اللہ دینے والا ہے",
            "سبسکرائب کریں",
            "اللہ حافظ",
        ],
        "category": "Quran"
    },
    "mother_respect": {
        "title": "Respect for Mother",
        "title_urdu": "ماں کا مقام",
        "arabic_text": "الْجَنَّةُ تَحْتَ أَقْدَامِ الْأُمَّهَاتِ",
        "arabic_source": "Sunan an-Nasa'i 3104",
        "arabic_verified": True,
        "script_urdu": """نبی صلی اللہ علیہ وسلم نے فرمایا:
جنت ماں کے قدموں تلے ہے۔

سبحان اللہ!

ماں کا مقام کتنا بلند ہے۔

ایک صحابی نے پوچھا:
یا رسول اللہ، میرے حسن سلوک کا سب سے زیادہ حقدار کون ہے؟

آپ نے فرمایا: تمہاری ماں۔
پھر کون؟ تمہاری ماں۔
پھر کون؟ تمہاری ماں۔
پھر کون؟ تمہارے باپ۔

تین بار ماں کا نام لیا!

ماں نے نو مہینے پیٹ میں رکھا۔
تکلیف سہی۔
راتیں جاگی۔
اپنا آرام چھوڑا۔

ماں کی دعا رد نہیں ہوتی۔
ماں کی خدمت جنت کا راستہ ہے۔

آج ماں کے قدم چومیں۔
ماں سے معافی مانگیں۔
ماں کی دعائیں لیں۔

سبسکرائب کریں۔
اللہ حافظ۔""",
        "captions": [
            "نبی ﷺ نے فرمایا",
            "جنت ماں کے قدموں تلے ہے",
            "سبحان اللہ!",
            "ماں کا مقام کتنا بلند ہے",
            "میرے حسن سلوک کا حقدار کون؟",
            "تمہاری ماں، تمہاری ماں، تمہاری ماں",
            "پھر تمہارے باپ",
            "تین بار ماں کا نام لیا!",
            "ماں نے نو مہینے پیٹ میں رکھا",
            "راتیں جاگی، تکلیف سہی",
            "ماں کی دعا رد نہیں ہوتی",
            "ماں کی خدمت جنت کا راستہ ہے",
            "آج ماں کے قدم چومیں",
            "سبسکرائب کریں",
            "اللہ حافظ",
        ],
        "category": "Hadith"
    },
    "tawakkul": {
        "title": "Trust in Allah",
        "title_urdu": "اللہ پر توکل",
        "arabic_text": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ",
        "arabic_source": "Surah At-Talaq 65:3",
        "arabic_verified": True,
        "script_urdu": """اللہ تعالیٰ فرماتے ہیں:
جو اللہ پر توکل کرے، اللہ اسے کافی ہے۔

توکل کیا ہے؟
اللہ پر بھروسہ کرنا۔
اللہ کی تدبیر پر یقین رکھنا۔

جب پریشانی ہو،
یاد رکھیں: اللہ کافی ہے۔

جب راستہ بند لگے،
یاد رکھیں: اللہ کافی ہے۔

جب لوگ ساتھ چھوڑ دیں،
یاد رکھیں: اللہ کافی ہے۔

نبی صلی اللہ علیہ وسلم نے فرمایا:
اگر تم اللہ پر سچا توکل کرو،
تو اللہ تمہیں ایسے رزق دے گا
جیسے پرندوں کو دیتا ہے۔

پرندہ صبح خالی پیٹ نکلتا ہے،
شام کو پیٹ بھر کر لوٹتا ہے۔

اللہ پر بھروسہ رکھیں۔
محنت کریں۔
نتیجہ اللہ پر چھوڑیں۔

حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ

سبسکرائب کریں۔
اللہ حافظ۔""",
        "captions": [
            "اللہ تعالیٰ فرماتے ہیں",
            "جو اللہ پر توکل کرے، اللہ اسے کافی ہے",
            "توکل کیا ہے؟",
            "اللہ پر بھروسہ کرنا",
            "جب پریشانی ہو - اللہ کافی ہے",
            "جب راستہ بند لگے - اللہ کافی ہے",
            "جب لوگ ساتھ چھوڑ دیں - اللہ کافی ہے",
            "نبی ﷺ نے فرمایا",
            "اگر سچا توکل کرو",
            "اللہ ایسے رزق دے گا جیسے پرندوں کو",
            "محنت کریں، نتیجہ اللہ پر چھوڑیں",
            "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ",
            "سبسکرائب کریں",
            "اللہ حافظ",
        ],
        "category": "Quran"
    },
}

# ============== CUSTOM CSS ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Scheherazade+New:wght@400;700&display=swap');

    /* Main background */
    .stApp {
        background: linear-gradient(180deg, #0a0f1a 0%, #111827 50%, #0a0f1a 100%);
    }

    /* Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1e3a5f 0%, #0d253f 50%, #1e3a5f 100%);
        color: #ffd700;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,215,0,0.2);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: "☪";
        position: absolute;
        left: 30px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2rem;
        opacity: 0.6;
    }

    .main-header::after {
        content: "☪";
        position: absolute;
        right: 30px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2rem;
        opacity: 0.6;
    }

    /* Arabic text styling */
    .arabic-text {
        font-family: 'Scheherazade New', 'Amiri', serif;
        font-size: 2rem;
        text-align: center;
        color: #ffd700;
        direction: rtl;
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(30,58,95,0.8) 0%, rgba(13,37,63,0.8) 100%);
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(255,215,0,0.3);
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* Urdu text styling */
    .urdu-text {
        font-family: 'Amiri', serif;
        font-size: 1.4rem;
        text-align: right;
        direction: rtl;
        line-height: 2.2;
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(20,30,50,0.9) 0%, rgba(30,40,60,0.9) 100%);
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        color: #e0e0e0;
    }

    /* Preview box */
    .preview-box {
        background: linear-gradient(180deg, #050810 0%, #0f1724 50%, #050810 100%);
        border-radius: 20px;
        padding: 30px;
        min-height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255,215,0,0.2);
        box-shadow: inset 0 0 100px rgba(0,0,0,0.5);
    }

    .preview-box::before {
        content: "";
        position: absolute;
        top: 20px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: radial-gradient(circle, #ffd700 0%, transparent 70%);
        border-radius: 50%;
        opacity: 0.3;
    }

    /* Caption preview */
    .caption-preview {
        font-family: 'Amiri', serif;
        font-size: 1.6rem;
        color: white;
        text-align: center;
        padding: 20px 40px;
        background: rgba(0,0,0,0.85);
        border-radius: 15px;
        direction: rtl;
        max-width: 85%;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Template cards */
    .template-card {
        background: linear-gradient(135deg, #1a2744 0%, #0f1a2e 100%);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,215,0,0.2);
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .template-card:hover {
        border-color: #ffd700;
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(255,215,0,0.2);
    }

    /* Section headers */
    .section-header {
        color: #ffd700;
        font-size: 1.3rem;
        font-weight: bold;
        padding: 0.5rem 0;
        border-bottom: 2px solid rgba(255,215,0,0.3);
        margin-bottom: 1rem;
    }

    /* Status badges */
    .badge-verified {
        background: linear-gradient(135deg, #1e5631 0%, #2d7a46 100%);
        color: #90EE90;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
    }

    .badge-category {
        background: linear-gradient(135deg, #4a3f6b 0%, #6b5b95 100%);
        color: #e0d5f5;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(15,23,42,0.8);
        padding: 10px;
        border-radius: 15px;
    }

    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #1a2744 0%, #0f1a2e 100%);
        border-radius: 10px;
        padding: 12px 24px;
        color: #a0aec0;
        border: 1px solid transparent;
    }

    .stTabs [data-baseweb="tab"]:hover {
        border-color: rgba(255,215,0,0.3);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a7c 100%) !important;
        color: #ffd700 !important;
        border: 1px solid rgba(255,215,0,0.5) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a7c 100%);
        color: white;
        border: 1px solid rgba(255,215,0,0.3);
        border-radius: 10px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        border-color: #ffd700;
        box-shadow: 0 4px 15px rgba(255,215,0,0.2);
        transform: translateY(-1px);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #d4a017 0%, #b8860b 100%);
        color: #000;
        font-weight: bold;
    }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1724 0%, #1a2744 100%);
    }

    /* Islamic pattern overlay */
    .islamic-pattern {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        opacity: 0.03;
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffd700' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }

    /* Video timeline */
    .timeline-track {
        height: 50px;
        background: linear-gradient(90deg, #1a2744 0%, #0f1a2e 100%);
        border-radius: 10px;
        margin: 10px 0;
        position: relative;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .timeline-progress {
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        background: linear-gradient(90deg, #1e5631 0%, #2d7a46 100%);
        border-radius: 10px 0 0 10px;
        opacity: 0.8;
    }
</style>

<div class="islamic-pattern"></div>
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
        'text_style': 'centered',
        'text_animation': 'fade',
        'audio_path': None,
        'video_path': None,
    }

# ============== HEADER ==============
st.markdown('<div class="main-header">🕌 Halal Video Editor</div>', unsafe_allow_html=True)

# ============== SIDEBAR ==============
with st.sidebar:
    st.markdown("### ☪️ Quick Templates")
    st.markdown("---")

    # Template selection
    for key, template in TEMPLATES.items():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{template['title_urdu']}**")
                st.caption(f"{template['title']} • {template['category']}")
            with col2:
                if st.button("Load", key=f"load_{key}", use_container_width=True):
                    st.session_state.project.update(template)
                    st.success("Template loaded!")
                    st.rerun()
            st.markdown("---")

    st.markdown("### 💾 Project")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save", use_container_width=True):
            project_path = OUTPUT_DIR / "project.json"
            with open(project_path, 'w', encoding='utf-8') as f:
                json.dump(st.session_state.project, f, ensure_ascii=False, indent=2)
            st.success("Saved!")

    with col2:
        if st.button("📂 Load", use_container_width=True):
            project_path = OUTPUT_DIR / "project.json"
            if project_path.exists():
                with open(project_path, 'r', encoding='utf-8') as f:
                    st.session_state.project = json.load(f)
                st.success("Loaded!")
                st.rerun()

    st.markdown("---")

    if st.button("📁 Open Output Folder", use_container_width=True):
        os.system(f'open "{OUTPUT_DIR}"')

# ============== MAIN TABS ==============
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Content",
    "🎙️ Audio",
    "🎨 Visuals",
    "▶️ Preview",
    "📤 Export"
])

# ============== TAB 1: CONTENT ==============
with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-header">📌 Video Information</div>', unsafe_allow_html=True)

        st.session_state.project['title'] = st.text_input(
            "English Title",
            value=st.session_state.project.get('title', ''),
            placeholder="e.g., The Power of Smiling in Islam"
        )

        st.session_state.project['title_urdu'] = st.text_input(
            "عنوان (Urdu Title)",
            value=st.session_state.project.get('title_urdu', ''),
            placeholder="مثال: مسکرانے کی طاقت"
        )

        st.markdown('<div class="section-header">📖 Arabic Text (Hadith/Ayat)</div>', unsafe_allow_html=True)

        st.session_state.project['arabic_text'] = st.text_area(
            "Arabic Text",
            value=st.session_state.project.get('arabic_text', ''),
            placeholder="تَبَسُّمُكَ فِي وَجْهِ أَخِيكَ صَدَقَةٌ",
            height=80
        )

        if st.session_state.project['arabic_text']:
            st.markdown(f'<div class="arabic-text">{st.session_state.project["arabic_text"]}</div>', unsafe_allow_html=True)

        st.session_state.project['arabic_source'] = st.text_input(
            "📚 Source Reference",
            value=st.session_state.project.get('arabic_source', ''),
            placeholder="e.g., Jami` at-Tirmidhi 1956"
        )

        st.session_state.project['arabic_verified'] = st.checkbox(
            "✅ I have verified this from authentic sources",
            value=st.session_state.project.get('arabic_verified', False)
        )

        if st.session_state.project['arabic_verified']:
            st.markdown('<span class="badge-verified">✓ Verified</span>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">📜 Script (Urdu)</div>', unsafe_allow_html=True)

        st.session_state.project['script_urdu'] = st.text_area(
            "اسکرپٹ لکھیں",
            value=st.session_state.project.get('script_urdu', ''),
            height=350,
            placeholder="""رسول اللہ صلی اللہ علیہ وسلم نے فرمایا:
اپنے بھائی کے سامنے مسکرانا صدقہ ہے۔

آج ہم اس خوبصورت حدیث کو سمجھیں گے..."""
        )

        if st.session_state.project['script_urdu']:
            st.markdown(f'<div class="urdu-text">{st.session_state.project["script_urdu"][:400]}...</div>', unsafe_allow_html=True)

    # Captions
    st.markdown("---")
    st.markdown('<div class="section-header">💬 Captions/Subtitles</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1.5])

    with col1:
        if st.button("🔄 Auto-Generate Captions", use_container_width=True):
            script = st.session_state.project.get('script_urdu', '')
            if script and len(script) > 10:
                lines = [l.strip() for l in script.split('\n') if l.strip() and len(l.strip()) > 5]
                if lines:
                    st.session_state.project['captions'] = lines
                    st.toast(f"✅ Generated {len(lines)} captions!", icon="✅")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Script mein koi valid lines nahi hain!")
            else:
                st.error("⚠️ Pehle script add karein!")

    with col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.project['captions'] = []
            st.toast("Captions cleared!", icon="🗑️")
            st.rerun()

    with col3:
        st.metric("Total", len(st.session_state.project.get('captions', [])))

    # Show captions
    captions = st.session_state.project.get('captions', [])
    if captions:
        st.markdown(f"**📋 {len(captions)} Captions Ready:**")
        with st.container(height=200):
            for i, cap in enumerate(captions):
                st.markdown(f'<div style="direction:rtl; text-align:right; padding:8px; margin:3px 0; background:rgba(30,58,95,0.5); border-radius:8px; border-right:3px solid #ffd700;">{i+1}. {cap}</div>', unsafe_allow_html=True)
    else:
        st.info("💡 Script likhein aur 'Auto-Generate Captions' click karein")


# ============== TAB 2: AUDIO ==============
with tab2:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-header">🎙️ Voice Settings</div>', unsafe_allow_html=True)

        voice_options = {
            "🇵🇰 Urdu - Male (Asad)": "ur-PK-AsadNeural",
            "🇵🇰 Urdu - Female (Uzma)": "ur-PK-UzmaNeural",
            "🇸🇦 Arabic - Male (Hamed)": "ar-SA-HamedNeural",
            "🇸🇦 Arabic - Female (Zariyah)": "ar-SA-ZariyahNeural",
            "🇮🇳 Hindi - Male (Madhur)": "hi-IN-MadhurNeural",
            "🇮🇳 Hindi - Female (Swara)": "hi-IN-SwaraNeural",
        }

        selected_voice = st.selectbox("Select Voice", list(voice_options.keys()))
        st.session_state.project['voice'] = voice_options[selected_voice]

        speed = st.slider("🏃 Speed", min_value=-30, max_value=30, value=-5, step=5,
                         help="Negative = slower, Positive = faster")
        st.session_state.project['voice_speed'] = f"{speed:+d}%"

        st.markdown("---")

        st.markdown('<div class="section-header">📤 Or Upload Audio</div>', unsafe_allow_html=True)

        uploaded_audio = st.file_uploader("Upload MP3/WAV", type=['mp3', 'wav'])

        if uploaded_audio:
            audio_path = OUTPUT_DIR / f"uploaded_{uploaded_audio.name}"
            with open(audio_path, 'wb') as f:
                f.write(uploaded_audio.read())
            st.session_state.project['audio_path'] = str(audio_path)
            st.success(f"✅ Uploaded: {uploaded_audio.name}")

    with col2:
        st.markdown('<div class="section-header">🔊 Audio Preview</div>', unsafe_allow_html=True)

        if st.button("🎵 Generate Voice", type="primary", use_container_width=True):
            if st.session_state.project['script_urdu']:
                with st.spinner("🎙️ Generating voice..."):
                    try:
                        import edge_tts

                        preview_path = OUTPUT_DIR / "voice_preview.mp3"

                        async def gen_voice():
                            communicate = edge_tts.Communicate(
                                text=st.session_state.project['script_urdu'],
                                voice=st.session_state.project['voice'],
                                rate=st.session_state.project['voice_speed']
                            )
                            await communicate.save(str(preview_path))

                        asyncio.run(gen_voice())
                        st.session_state.project['audio_path'] = str(preview_path)
                        st.success("✅ Voice generated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Please add script first!")

        audio_path = st.session_state.project.get('audio_path')
        if audio_path and os.path.exists(audio_path):
            st.audio(audio_path)
            file_size = os.path.getsize(audio_path) / 1024
            st.caption(f"📁 {os.path.basename(audio_path)} ({file_size:.1f} KB)")


# ============== TAB 3: VISUALS ==============
with tab3:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-header">🖼️ Background</div>', unsafe_allow_html=True)

        bg_type = st.radio(
            "Background Type",
            ["🌙 Animated (Stars & Moon)", "🌿 Nature Videos", "🎨 Solid Color"],
            index=0
        )

        st.session_state.project['bg_type'] = bg_type

        if "Animated" in bg_type:
            anim_style = st.selectbox(
                "Animation Style",
                ["Starfield with Crescent Moon", "Floating Particles", "Geometric Islamic Pattern"]
            )

        elif "Nature" in bg_type:
            st.info("🔑 Pexels API key needed for nature videos")
            pexels_key = st.text_input("Pexels API Key", type="password")

        else:
            bg_color = st.color_picker("Background Color", "#0f1724")

        st.slider("🔅 Background Brightness", 0, 100, 30, help="Lower = darker background")

    with col2:
        st.markdown('<div class="section-header">✨ Text Style</div>', unsafe_allow_html=True)

        text_position = st.selectbox(
            "Caption Position",
            ["Center (TikTok/Reels style)", "Bottom", "Top"],
            index=0
        )

        text_animation = st.selectbox(
            "Animation Style",
            ["Word by Word (Karaoke)", "Fade In/Out", "Slide Up", "Typewriter"],
            index=0
        )

        st.markdown("---")

        font_size = st.slider("📝 Font Size", 24, 72, 42)
        text_color = st.color_picker("Text Color", "#FFFFFF")

        show_bg = st.checkbox("Show text background", value=True)
        if show_bg:
            bg_opacity = st.slider("Background Opacity", 0, 100, 80)


# ============== TAB 4: PREVIEW ==============
with tab4:
    st.markdown('<div class="section-header">▶️ Video Preview</div>', unsafe_allow_html=True)

    # Preview box
    arabic_text = st.session_state.project.get('arabic_text', 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ')
    title_urdu = st.session_state.project.get('title_urdu', 'عنوان')
    sample_caption = st.session_state.project.get('captions', ['مثال کیپشن'])[0] if st.session_state.project.get('captions') else 'مثال کیپشن'

    st.markdown(f"""
    <div class="preview-box">
        <div style="color: #ffd700; font-family: 'Scheherazade New', serif; font-size: 1.8rem; margin-bottom: 15px; direction: rtl; text-shadow: 0 2px 10px rgba(255,215,0,0.5);">
            {arabic_text}
        </div>
        <div style="color: #a0a0a0; font-size: 0.9rem; margin-bottom: 30px;">
            {st.session_state.project.get('arabic_source', '')}
        </div>
        <div class="caption-preview">
            {sample_caption}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Timeline
    st.markdown('<div class="section-header">⏱️ Timeline</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="timeline-track">
        <div class="timeline-progress" style="width: 35%;"></div>
    </div>
    """, unsafe_allow_html=True)

    captions = st.session_state.project.get('captions', [])
    if captions:
        st.caption(f"📝 {len(captions)} captions will be displayed")


# ============== TAB 5: EXPORT ==============
with tab5:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-header">⚙️ Export Settings</div>', unsafe_allow_html=True)

        resolution = st.selectbox(
            "Resolution",
            ["1080p (1920×1080) - YouTube", "720p (1280×720)", "9:16 (1080×1920) - TikTok/Reels"]
        )

        quality = st.selectbox(
            "Quality",
            ["High Quality", "Medium (Balanced)", "Low (Smaller file)"]
        )

        st.markdown("---")

        st.markdown("### ✅ Checklist")

        project = st.session_state.project
        checks = {
            "Title": bool(project.get('title') or project.get('title_urdu')),
            "Arabic Text": bool(project.get('arabic_text')),
            "Arabic Verified": project.get('arabic_verified', False),
            "Script": bool(project.get('script_urdu')),
            "Audio": bool(project.get('audio_path') and os.path.exists(project.get('audio_path', ''))),
            "Captions": len(project.get('captions', [])) > 0,
        }

        for item, status in checks.items():
            if status:
                st.markdown(f"✅ {item}")
            else:
                st.markdown(f"⬜ {item}")

    with col2:
        st.markdown('<div class="section-header">🎬 Generate Video</div>', unsafe_allow_html=True)

        ready = sum(checks.values()) >= 3  # At least 3 items checked (more lenient)

        if ready:
            if st.button("🚀 Generate Video", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    from generate_video import generate_video

                    def update_progress(pct, msg):
                        progress_bar.progress(pct)
                        status_text.text(msg)

                    # Generate unique filename
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_name = f"halal_video_{timestamp}"

                    # Get project data
                    proj = st.session_state.project

                    # Generate the video
                    video_path, audio_path = generate_video(
                        script_urdu=proj.get('script_urdu', ''),
                        title_urdu=proj.get('title_urdu', ''),
                        arabic_text=proj.get('arabic_text', ''),
                        captions=proj.get('captions', []),
                        voice=proj.get('voice', 'ur-PK-AsadNeural'),
                        voice_speed=proj.get('voice_speed', '-5%'),
                        output_name=output_name,
                        progress_callback=update_progress
                    )

                    st.success("🎉 Video generated successfully!")

                    # Show video
                    st.video(str(video_path))

                    # Download button
                    with open(video_path, 'rb') as f:
                        st.download_button(
                            "⬇️ Download Video",
                            f,
                            file_name=f"{output_name}.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )

                    # File info
                    size_mb = os.path.getsize(video_path) / (1024*1024)
                    st.caption(f"📁 {video_path.name} ({size_mb:.1f} MB)")

                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    import traceback
                    st.code(traceback.format_exc())
        else:
            st.warning("⚠️ Please complete required fields:")

            missing = [k for k, v in checks.items() if not v]
            for item in missing:
                st.markdown(f"• {item}")

    st.markdown("---")

    # Previous videos
    st.markdown('<div class="section-header">📂 Previous Videos</div>', unsafe_allow_html=True)

    video_files = list(OUTPUT_DIR.glob("*.mp4"))
    if video_files:
        for vf in sorted(video_files, key=os.path.getmtime, reverse=True)[:3]:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.text(vf.name)
            with col2:
                size = os.path.getsize(vf) / (1024*1024)
                st.text(f"{size:.1f} MB")
            with col3:
                if st.button("▶️", key=f"play_{vf.name}"):
                    st.video(str(vf))
    else:
        st.info("No videos generated yet")


# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>☪️ Halal Video Editor • Professional Islamic Content Creator</p>",
    unsafe_allow_html=True
)
