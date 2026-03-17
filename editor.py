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
import nest_asyncio

# Fix asyncio for Streamlit
nest_asyncio.apply()

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config import OUTPUT_DIR, ASSETS_DIR
from src.content_categories import CONTENT_CATEGORIES, get_category, list_categories
from src.script_generator import get_script_generator

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
    "shukr_gratitude": {
        "title": "Gratitude to Allah",
        "title_urdu": "شکر کی فضیلت",
        "arabic_text": "لَئِن شَكَرْتُمْ لَأَزِيدَنَّكُمْ",
        "arabic_source": "Surah Ibrahim 14:7",
        "arabic_verified": True,
        "script_urdu": """اللہ تعالیٰ فرماتے ہیں:
اگر تم شکر کرو گے تو میں تمہیں اور زیادہ دوں گا۔

سبحان اللہ! کتنا بڑا وعدہ ہے۔

شکر کا مطلب کیا ہے؟
اللہ کی نعمتوں کو پہچاننا۔
دل سے ان کا اعتراف کرنا۔
زبان سے الحمد للہ کہنا۔

ہم کتنی نعمتوں میں ہیں!
صحت، خاندان، کھانا، پانی۔
ہر سانس اللہ کی نعمت ہے۔

نبی صلی اللہ علیہ وسلم نے فرمایا:
جس نے صبح کی اور اس کا جسم صحیح ہے،
اور اس کے پاس ایک دن کا کھانا ہے،
گویا اسے ساری دنیا مل گئی۔

الحمد للہ کہیں۔
ہر حال میں شکر کریں۔

سبسکرائب کریں۔
اللہ حافظ۔""",
        "captions": [
            "اللہ تعالیٰ فرماتے ہیں",
            "اگر شکر کرو گے تو میں زیادہ دوں گا",
            "سبحان اللہ! کتنا بڑا وعدہ",
            "شکر کا مطلب کیا ہے؟",
            "اللہ کی نعمتوں کو پہچاننا",
            "ہم کتنی نعمتوں میں ہیں!",
            "صحت، خاندان، کھانا، پانی",
            "ہر سانس اللہ کی نعمت ہے",
            "نبی ﷺ نے فرمایا",
            "الحمد للہ کہیں",
            "ہر حال میں شکر کریں",
            "سبسکرائب کریں",
        ],
        "category": "Quran"
    },
    "istighfar": {
        "title": "Power of Istighfar",
        "title_urdu": "استغفار کی طاقت",
        "arabic_text": "وَمَن يَعْمَلْ سُوءًا أَوْ يَظْلِمْ نَفْسَهُ ثُمَّ يَسْتَغْفِرِ اللَّهَ يَجِدِ اللَّهَ غَفُورًا رَّحِيمًا",
        "arabic_source": "Surah An-Nisa 4:110",
        "arabic_verified": True,
        "script_urdu": """اللہ تعالیٰ فرماتے ہیں:
جو کوئی برا کام کرے یا اپنے آپ پر ظلم کرے،
پھر اللہ سے معافی مانگے،
تو وہ اللہ کو بخشنے والا مہربان پائے گا۔

استغفار کی طاقت بے حد ہے۔
گناہوں سے پاک ہونے کا راستہ۔
رزق میں برکت کا ذریعہ۔
پریشانیوں سے نجات۔

نبی صلی اللہ علیہ وسلم نے فرمایا:
جو استغفار کو لازم پکڑ لے،
اللہ اسے ہر تنگی سے نکال دیتے ہیں۔
ہر غم سے راحت دیتے ہیں۔
اور جہاں سے گمان نہ ہو، رزق دیتے ہیں۔

أَسْتَغْفِرُ اللَّهَ
میں اللہ سے معافی مانگتا ہوں۔

روزانہ کم از کم سو بار استغفار کریں۔

سبسکرائب کریں۔
اللہ حافظ۔""",
        "captions": [
            "اللہ تعالیٰ فرماتے ہیں",
            "جو اللہ سے معافی مانگے",
            "اللہ کو بخشنے والا مہربان پائے گا",
            "استغفار کی طاقت بے حد ہے",
            "گناہوں سے پاک ہونے کا راستہ",
            "نبی ﷺ نے فرمایا",
            "جو استغفار کو لازم پکڑ لے",
            "اللہ ہر تنگی سے نکال دیتے ہیں",
            "جہاں سے گمان نہ ہو، رزق دیتے ہیں",
            "أَسْتَغْفِرُ اللَّهَ",
            "روزانہ سو بار استغفار کریں",
            "سبسکرائب کریں",
        ],
        "category": "Quran"
    },
    "durood_sharif": {
        "title": "Blessings of Durood",
        "title_urdu": "درود شریف کی فضیلت",
        "arabic_text": "إِنَّ اللَّهَ وَمَلَائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ",
        "arabic_source": "Surah Al-Ahzab 33:56",
        "arabic_verified": True,
        "script_urdu": """اللہ تعالیٰ فرماتے ہیں:
بے شک اللہ اور اس کے فرشتے نبی پر درود بھیجتے ہیں۔

اے ایمان والو!
تم بھی ان پر درود اور سلام بھیجو۔

نبی صلی اللہ علیہ وسلم نے فرمایا:
جو مجھ پر ایک بار درود بھیجے،
اللہ اس پر دس رحمتیں نازل فرماتے ہیں۔

اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ
وَعَلَى آلِ مُحَمَّدٍ

جمعہ کا دن درود کا خاص دن ہے۔
کثرت سے درود پڑھیں۔

درود سے گناہ معاف ہوتے ہیں۔
درود سے پریشانیاں دور ہوتی ہیں۔
درود سے قیامت کے دن شفاعت ملے گی۔

سبسکرائب کریں۔
اللہ حافظ۔""",
        "captions": [
            "اللہ اور فرشتے نبی ﷺ پر درود بھیجتے ہیں",
            "اے ایمان والو! تم بھی درود بھیجو",
            "نبی ﷺ نے فرمایا",
            "ایک درود پر دس رحمتیں",
            "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ",
            "جمعہ کا دن درود کا خاص دن ہے",
            "کثرت سے درود پڑھیں",
            "درود سے گناہ معاف ہوتے ہیں",
            "درود سے پریشانیاں دور ہوتی ہیں",
            "سبسکرائب کریں",
        ],
        "category": "Hadith"
    },
    "namaz_importance": {
        "title": "Importance of Prayer",
        "title_urdu": "نماز کی اہمیت",
        "arabic_text": "إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ",
        "arabic_source": "Surah Al-Ankabut 29:45",
        "arabic_verified": True,
        "script_urdu": """اللہ تعالیٰ فرماتے ہیں:
بے شک نماز بے حیائی اور برے کاموں سے روکتی ہے۔

نماز دین کا ستون ہے۔
نماز مومن کی معراج ہے۔
نماز اللہ سے سیدھا رابطہ ہے۔

نبی صلی اللہ علیہ وسلم نے فرمایا:
قیامت کے دن سب سے پہلے نماز کا حساب ہوگا۔
اگر نماز درست ہوئی تو سب درست۔
اگر نماز خراب ہوئی تو سب خراب۔

پانچ نمازیں لازم ہیں۔
فجر، ظہر، عصر، مغرب، عشاء۔

نماز وقت پر پڑھیں۔
نماز جماعت سے پڑھیں۔
نماز خشوع سے پڑھیں۔

سبسکرائب کریں۔
اللہ حافظ۔""",
        "captions": [
            "نماز بے حیائی سے روکتی ہے",
            "نماز دین کا ستون ہے",
            "نماز مومن کی معراج ہے",
            "نبی ﷺ نے فرمایا",
            "قیامت کے دن پہلے نماز کا حساب",
            "نماز درست تو سب درست",
            "پانچ نمازیں لازم ہیں",
            "فجر، ظہر، عصر، مغرب، عشاء",
            "نماز وقت پر پڑھیں",
            "نماز جماعت سے پڑھیں",
            "سبسکرائب کریں",
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
        'tts_provider': 'edge',
        'voice': 'ur-PK-AsadNeural',
        'voice_speed': '-22%',  # Slower = storytelling style
        'urdu_pitch': '-15Hz',  # Deeper = calmer, natural
        'arabic_voice': 'ar-SA-HamedNeural',
        'arabic_pitch': '-8Hz',  # Slightly deeper Arabic
        'include_arabic_recitation': True,
        'bg_type': 'animated',
        'text_style': 'centered',
        'text_effect': 'fade',
        'audio_path': None,
        'video_path': None,
        'content_category': 'halal',  # Default category
    }

# ============== HEADER ==============
st.markdown('<div class="main-header">🕌 Halal Video Editor</div>', unsafe_allow_html=True)

# ============== SIDEBAR ==============
with st.sidebar:
    st.markdown("### 🎬 Content Category")

    # Category selector with visual styling
    category_options = {cat_id: cat_data["name"] for cat_id, cat_data in CONTENT_CATEGORIES.items()}

    selected_category = st.selectbox(
        "Choose Category",
        options=list(category_options.keys()),
        format_func=lambda x: category_options[x],
        index=list(category_options.keys()).index(st.session_state.project.get('content_category', 'halal')),
        label_visibility="collapsed"
    )

    # Update session state
    st.session_state.project['content_category'] = selected_category

    # Show category info
    cat_info = get_category(selected_category)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a2744 0%, #0f1a2e 100%);
                padding: 10px; border-radius: 10px; margin: 8px 0;
                border: 1px solid rgba(255,215,0,0.2); font-size: 0.85rem;">
        <div style="color: #888;">
            {cat_info['description']}
        </div>
        <div style="color: #666; margin-top: 5px; font-size: 0.75rem;">
            Mood: {cat_info['mood']} | Style: {cat_info['scenery']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ============ AUTO GENERATE SCRIPT ============
    st.markdown("### 🎲 Auto Generate Script")

    script_gen = get_script_generator()
    current_category = st.session_state.project.get('content_category', 'halal')

    # Show available templates for this category
    template_titles = script_gen.get_template_titles(current_category)

    if template_titles:
        st.markdown(f"**{len(template_titles)} scripts available for {cat_info['name']}**")

        # Random generate button
        if st.button("🎲 Generate Random Script", use_container_width=True, type="primary"):
            new_script = script_gen.generate_script(current_category)
            st.session_state.project['title_urdu'] = new_script['title_urdu']
            st.session_state.project['script_urdu'] = new_script['script_urdu']
            st.session_state.project['arabic_text'] = new_script.get('arabic_text', '')
            st.session_state.project['arabic_source'] = new_script.get('arabic_source', '')
            # Auto-generate captions
            lines = [l.strip() for l in new_script['script_urdu'].split('\n') if l.strip() and len(l.strip()) > 5]
            st.session_state.project['captions'] = lines
            st.toast(f"✅ Generated: {new_script['title_urdu']}", icon="🎲")
            st.rerun()

        # Select specific template
        selected_title = st.selectbox(
            "Or choose specific script",
            [""] + template_titles,
            format_func=lambda x: x if x else "-- Select --"
        )

        if selected_title:
            if st.button(f"📥 Load: {selected_title}", use_container_width=True):
                new_script = script_gen.get_template_by_title(current_category, selected_title)
                st.session_state.project['title_urdu'] = new_script['title_urdu']
                st.session_state.project['script_urdu'] = new_script['script_urdu']
                st.session_state.project['arabic_text'] = new_script.get('arabic_text', '')
                st.session_state.project['arabic_source'] = new_script.get('arabic_source', '')
                lines = [l.strip() for l in new_script['script_urdu'].split('\n') if l.strip() and len(l.strip()) > 5]
                st.session_state.project['captions'] = lines
                st.toast(f"✅ Loaded: {selected_title}", icon="✅")
                st.rerun()

    st.markdown("---")

    st.markdown("### ☪️ Islamic Templates")

    # Template dropdown selection (for Islamic only)
    islamic_templates = {key: f"{t['title_urdu']} - {t['title']}" for key, t in TEMPLATES.items()}
    islamic_templates = {"": "-- Select Template --", **islamic_templates}

    selected_template = st.selectbox(
        "Choose Template",
        options=list(islamic_templates.keys()),
        format_func=lambda x: islamic_templates[x],
        label_visibility="collapsed"
    )

    if selected_template and selected_template in TEMPLATES:
        template = TEMPLATES[selected_template]
        if st.button("📥 Load This Template", use_container_width=True):
            st.session_state.project.update(template)
            st.toast("✅ Template loaded!", icon="✅")
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

        # Only show Arabic section for Islamic category
        is_islamic_category = st.session_state.project.get('content_category', 'halal') == 'halal'

        if is_islamic_category:
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
        else:
            # Clear Arabic fields for non-Islamic categories
            st.session_state.project['arabic_text'] = ''
            st.session_state.project['arabic_source'] = ''
            st.session_state.project['include_arabic_recitation'] = False

    with col2:
        st.markdown('<div class="section-header">📜 Script (Urdu)</div>', unsafe_allow_html=True)

        # RTL text area with custom styling
        st.markdown("""
        <style>
        textarea[aria-label="اسکرپٹ لکھیں"] {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Amiri', serif !important;
            font-size: 1.1rem !important;
            line-height: 2 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.session_state.project['script_urdu'] = st.text_area(
            "اسکرپٹ لکھیں",
            value=st.session_state.project.get('script_urdu', ''),
            height=300,
            placeholder="""رسول اللہ صلی اللہ علیہ وسلم نے فرمایا:
اپنے بھائی کے سامنے مسکرانا صدقہ ہے۔

آج ہم اس خوبصورت حدیث کو سمجھیں گے..."""
        )

        # Copy button and script preview
        if st.session_state.project['script_urdu']:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                if st.button("📋 Copy Script", use_container_width=True):
                    st.code(st.session_state.project['script_urdu'], language=None)
                    st.toast("Script shown above - Select & Copy!", icon="📋")
            with col_b:
                word_count = len(st.session_state.project['script_urdu'].split())
                st.metric("Words", word_count)

            # RTL preview
            st.markdown(f'''
            <div style="direction: rtl; text-align: right; padding: 15px;
                        background: linear-gradient(135deg, rgba(20,30,50,0.9) 0%, rgba(30,40,60,0.9) 100%);
                        border-radius: 10px; border: 1px solid rgba(255,215,0,0.2);
                        font-family: 'Amiri', serif; font-size: 1.1rem; line-height: 2;
                        color: #e0e0e0; max-height: 200px; overflow-y: auto;">
                {st.session_state.project["script_urdu"]}
            </div>
            ''', unsafe_allow_html=True)

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
        st.markdown('<div class="section-header">🎙️ Voice Settings (FREE)</div>', unsafe_allow_html=True)

        # Show category voice recommendation
        current_cat = get_category(st.session_state.project.get('content_category', 'halal'))
        cat_voices = current_cat.get('voices', {})
        if cat_voices:
            recommended_voice = cat_voices.get('urdu', 'ur-PK-AsadNeural')
            st.markdown(f"""
            <div style="background: rgba(30,58,95,0.4); padding: 10px; border-radius: 8px; margin-bottom: 10px;
                        border-left: 3px solid #ffd700; font-size: 0.85rem;">
                <span style="color: #ffd700;">Category:</span> {current_cat['name']}<br>
                <span style="color: #888;">Recommended voice style for {current_cat['mood']} mood</span>
            </div>
            """, unsafe_allow_html=True)

        st.session_state.project['tts_provider'] = 'edge'  # Always Edge TTS (free)

        # Voice options based on category
        is_kids_category = st.session_state.project.get('content_category') == 'kids'

        # Different voice options for kids vs other categories
        if is_kids_category:
            st.markdown("**🎙️ Voice Selection** (Kids - Female recommended)")
            urdu_voice_options = {
                "🇵🇰 Uzma (Female - Kids Recommended)": "ur-PK-UzmaNeural",
                "🇵🇰 Asad (Male)": "ur-PK-AsadNeural",
            }
        else:
            st.markdown("**🎙️ Voice Selection**")
            urdu_voice_options = {
                "🇵🇰 Asad (Pakistan - Recommended)": "ur-PK-AsadNeural",
                "🇮🇳 Salman (India)": "ur-IN-SalmanNeural",
                "🇵🇰 Uzma (Female)": "ur-PK-UzmaNeural",
            }

        selected_urdu_voice = st.selectbox("Urdu Voice", list(urdu_voice_options.keys()))
        st.session_state.project['voice'] = urdu_voice_options[selected_urdu_voice]

        st.markdown("**⚙️ Natural Voice Settings**")

        speed = st.slider("🏃 Speech Speed", min_value=-35, max_value=-10, value=-22, step=1,
                         help="-20% to -28% sounds most natural for storytelling")
        st.session_state.project['voice_speed'] = f"{speed:+d}%"

        urdu_pitch = st.slider("🔊 Voice Depth", min_value=-25, max_value=-8, value=-15, step=1,
                              help="-15Hz to -20Hz for deeper, calmer male voice")
        st.session_state.project['urdu_pitch'] = f"{urdu_pitch:+d}Hz"

        st.info("""
        💡 **Natural Voice Tips:**
        - Speed: -20% to -28% (slower = storytelling style)
        - Pitch: -15Hz to -20Hz (deeper = natural calm)
        - System automatically adds pauses at punctuation
        - Use "..." in script for extra pauses
        """)

        st.markdown("---")

        # Only show Arabic recitation for Islamic category
        is_islamic = st.session_state.project.get('content_category', 'halal') == 'halal'

        if is_islamic:
            st.markdown('<div class="section-header">📖 Arabic Recitation</div>', unsafe_allow_html=True)

            include_arabic = st.checkbox(
                "✅ Include Arabic Recitation",
                value=st.session_state.project.get('include_arabic_recitation', True),
                help="Pehle Arabic hadith/ayat recite hogi"
            )
            st.session_state.project['include_arabic_recitation'] = include_arabic

            if include_arabic:
                st.markdown("**📖 Arabic Male Voices**")

                arabic_voice_options = {
                    "🇸🇦 Hamed (Saudi) - Qari Style": "ar-SA-HamedNeural",
                    "🇪🇬 Shakir (Egyptian)": "ar-EG-ShakirNeural",
                    "🇦🇪 Hamdan (UAE)": "ar-AE-HamdanNeural",
                }

                selected_arabic_voice = st.selectbox("Arabic Voice", list(arabic_voice_options.keys()))
                st.session_state.project['arabic_voice'] = arabic_voice_options[selected_arabic_voice]

                arabic_pitch = st.slider("🎵 Arabic Voice Depth", min_value=-15, max_value=0, value=-5, step=1)
                st.session_state.project['arabic_pitch'] = f"{arabic_pitch:+d}Hz"

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
        st.markdown('<div class="section-header">🖼️ Background Style</div>', unsafe_allow_html=True)

        # Get current category info
        current_cat = get_category(st.session_state.project.get('content_category', 'halal'))
        cat_name = current_cat['name']
        cat_scenery = current_cat['scenery']

        # Show category-based scenery
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(30,58,95,0.6) 0%, rgba(13,37,63,0.6) 100%);
                    padding: 15px; border-radius: 12px; margin-bottom: 15px;
                    border: 1px solid rgba(255,215,0,0.3);">
            <div style="color: #ffd700; font-size: 1.1rem; margin-bottom: 8px;">
                {cat_name}
            </div>
            <div style="color: #aaa; font-size: 0.9rem;">
                Scenery: <span style="color: #8aff8a;">{cat_scenery}</span>
            </div>
            <div style="color: #888; font-size: 0.8rem; margin-top: 5px;">
                Elements: {', '.join(current_cat['elements'][:4])}...
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Background mode options
        bg_mode_options = {
            "🎬 Category Scenery (Animated backgrounds)": "scenery",
            "🌈 Dynamic (Changes with content keywords)": "dynamic",
            "🌙 Classic Night (Stars & Moon)": "animated",
            "🎨 Static (Simple gradient)": "static",
        }

        selected_bg = st.radio(
            "Background Mode",
            list(bg_mode_options.keys()),
            index=0,
            help="Category scenery uses animated backgrounds based on your selected content type"
        )
        st.session_state.project['bg_mode'] = bg_mode_options[selected_bg]

        if "Category" in selected_bg:
            st.success(f"✨ Using {cat_scenery} scenery!")
            st.markdown(f"""
            **Category Scenery Styles:**
            - 🕌 **halal**: Islamic village with mosque, minarets, stars
            - 👻 **horror**: Dark fog, bats, abandoned houses
            - 🔍 **mystery**: Noir city, rain, streetlights
            - 🧒 **kids**: Sunny village, butterflies, rainbow
            - 💪 **motivational**: Sunrise mountains, birds
            - 📜 **history**: Ancient ruins, torches
            - 🔬 **science**: Space, planets, nebula
            - 💕 **poetry**: Moonlit garden, roses
            - 📰 **facts**: Minimal, clean
            - 🎮 **gaming**: Neon cyber grid
            """)
        elif "Dynamic" in selected_bg:
            st.info("🌈 Colors change based on content keywords")
        elif "Classic" in selected_bg:
            st.info("🌙 Classic Islamic starfield with crescent moon")
        else:
            st.info("🎨 Simple gradient background")

    with col2:
        st.markdown('<div class="section-header">✨ Text Style</div>', unsafe_allow_html=True)

        text_position = st.selectbox(
            "Caption Position",
            ["Center (TikTok/Reels style)", "Bottom", "Top"],
            index=0
        )

        # Text effect mapping
        text_effect_options = {
            "Fade In/Out (Recommended)": "fade",
            "Word by Word (Karaoke)": "karaoke",
            "Typewriter Effect": "typewriter",
            "Slide from Left": "slide_left",
            "Slide from Right": "slide_right",
            "Slide Up": "slide_up",
            "Zoom In": "zoom",
            "No Animation": "none",
        }

        text_animation = st.selectbox(
            "Caption Animation Style",
            list(text_effect_options.keys()),
            index=0,
            help="Choose how captions appear on screen"
        )
        st.session_state.project['text_effect'] = text_effect_options[text_animation]

        st.markdown("---")

        font_size = st.slider("📝 Font Size", 24, 72, 42)
        text_color = st.color_picker("Text Color", "#FFFFFF")

        show_bg = st.checkbox("Show text background", value=True)
        if show_bg:
            bg_opacity = st.slider("Background Opacity", 0, 100, 80)

    # Background Audio Section
    st.markdown("---")
    st.markdown('<div class="section-header">🔊 Background Audio (ASMR)</div>', unsafe_allow_html=True)

    col_audio1, col_audio2 = st.columns([2, 1])

    with col_audio1:
        bg_audio_options = {
            "None": "",
            "🌬️ Wind / Breeze (Horror, Mystery)": "wind",
            "🌧️ Rain (Calm, Sad)": "rain",
            "🔥 Fire Crackle (Warm, Cozy)": "fire",
            "🌙 Night Ambient (Islamic, Poetry)": "night",
        }

        selected_bg_audio = st.selectbox(
            "Background Sound",
            list(bg_audio_options.keys()),
            index=0,
            help="Add ambient ASMR sound to your video"
        )
        st.session_state.project['background_audio'] = bg_audio_options[selected_bg_audio]

    with col_audio2:
        if st.session_state.project.get('background_audio'):
            bg_volume = st.slider("Volume", 10, 50, 30, help="Background audio volume %")
            st.session_state.project['background_volume'] = bg_volume / 100.0
        else:
            st.session_state.project['background_volume'] = 0.3

    # ============ CAPTION VISUALS (AI Images) ============
    st.markdown("---")
    st.markdown('<div class="section-header">🖼️ Caption Visuals (AI Images)</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(30,58,95,0.3); padding: 12px; border-radius: 10px; margin-bottom: 15px;
                border: 1px solid rgba(255,215,0,0.2); font-size: 0.9rem;">
        <b>AI Image Generation</b> - ہر caption کے لیے AI automatically matching image generate کرے گا۔
        Images will blend smoothly with the background during each caption.
    </div>
    """, unsafe_allow_html=True)

    col_vis1, col_vis2 = st.columns([2, 1])

    with col_vis1:
        auto_gen_images = st.checkbox(
            "🤖 Auto-Generate AI Images for Captions",
            value=st.session_state.project.get('auto_generate_images', False),
            help="AI will generate matching images for each caption (uses free Pollinations.ai API - may be slow)"
        )
        st.session_state.project['auto_generate_images'] = auto_gen_images

        if auto_gen_images:
            st.warning("⚠️ AI image generation is slow and may fail due to rate limits. Video will still work without images.")

    with col_vis2:
        if auto_gen_images:
            image_style_options = {
                "🎬 Cinematic": "cinematic",
                "👻 Dark/Horror": "dark",
                "✨ Fantasy": "fantasy",
                "📷 Realistic": "realistic",
                "🎨 Anime": "anime",
                "⬜ Minimal": "minimal",
            }
            selected_style = st.selectbox(
                "Image Style",
                list(image_style_options.keys()),
                index=0 if st.session_state.project.get('content_category') != 'horror' else 1
            )
            st.session_state.project['image_style'] = image_style_options[selected_style]

    if auto_gen_images:
        captions = st.session_state.project.get('captions', [])
        if captions:
            st.success(f"✨ AI will generate {len(captions)} images during video creation")
        else:
            st.warning("⚠️ Pehle captions add karein (Content tab mein)")


# ============== TAB 4: PREVIEW ==============
with tab4:
    st.markdown('<div class="section-header">▶️ Video Preview</div>', unsafe_allow_html=True)

    # Preview box - conditionally show Arabic for Islamic category only
    is_islamic_preview = st.session_state.project.get('content_category', 'halal') == 'halal'
    title_urdu = st.session_state.project.get('title_urdu', 'عنوان')
    sample_caption = st.session_state.project.get('captions', ['مثال کیپشن'])[0] if st.session_state.project.get('captions') else 'مثال کیپشن'

    if is_islamic_preview:
        arabic_text = st.session_state.project.get('arabic_text', 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ')
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
    else:
        # Non-Islamic preview - no Arabic, show title and caption only
        cat_info = get_category(st.session_state.project.get('content_category', 'halal'))
        st.markdown(f"""
        <div class="preview-box">
            <div style="color: #ffd700; font-size: 1.5rem; margin-bottom: 15px; direction: rtl; text-align: center;">
                {cat_info['name']}
            </div>
            <div style="color: #a0a0a0; font-size: 1.2rem; margin-bottom: 20px; direction: rtl; text-align: center;">
                {title_urdu}
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

        resolution_options = {
            "1080p (1920×1080) - YouTube": "1080p",
            "720p (1280×720)": "720p",
            "9:16 (1080×1920) - TikTok/Reels": "tiktok"
        }

        selected_res = st.selectbox(
            "Resolution",
            list(resolution_options.keys()),
            index=0
        )
        st.session_state.project['resolution'] = resolution_options[selected_res]

        quality = st.selectbox(
            "Quality",
            ["High Quality", "Medium (Balanced)", "Low (Smaller file)"]
        )

        if "TikTok" in selected_res:
            st.info("📱 Vertical video (9:16) for TikTok/Reels/Shorts")

        st.markdown("---")

        st.markdown("### ✅ Checklist")

        project = st.session_state.project
        is_islamic_export = project.get('content_category', 'halal') == 'halal'

        # Different checklist for Islamic vs other categories
        if is_islamic_export:
            checks = {
                "Title": bool(project.get('title') or project.get('title_urdu')),
                "Arabic Text": bool(project.get('arabic_text')),
                "Arabic Verified": project.get('arabic_verified', False),
                "Script": bool(project.get('script_urdu')),
                "Captions": len(project.get('captions', [])) > 0,
            }
        else:
            # Non-Islamic - no Arabic requirements
            checks = {
                "Title": bool(project.get('title') or project.get('title_urdu')),
                "Script": bool(project.get('script_urdu')),
                "Captions": len(project.get('captions', [])) > 0,
            }

        for item, status in checks.items():
            if status:
                st.markdown(f"✅ {item}")
            else:
                st.markdown(f"⬜ {item}")

    with col2:
        st.markdown('<div class="section-header">🎬 Generate Video</div>', unsafe_allow_html=True)

        # Check if script exists
        has_script = bool(st.session_state.project.get('script_urdu', '').strip())

        if not has_script:
            st.warning("⚠️ Pehle Content tab me script add karein!")

        # Always show button
        if st.button("🚀 GENERATE VIDEO", type="primary", use_container_width=True, disabled=not has_script):
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                status_text.text("🔄 Starting...")
                progress_bar.progress(5)

                from generate_video import generate_video

                def update_progress(pct, msg):
                    progress_bar.progress(min(pct, 100))
                    status_text.text(msg)

                # Generate unique filename
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_name = f"halal_video_{timestamp}"

                # Get project data
                proj = st.session_state.project

                # Check if user uploaded custom audio
                uploaded_audio_path = proj.get('audio_path')
                use_uploaded_audio = False
                if uploaded_audio_path and os.path.exists(uploaded_audio_path):
                    # Check if it's an uploaded audio (not generated voice preview)
                    if 'uploaded_' in os.path.basename(uploaded_audio_path):
                        use_uploaded_audio = True

                # Generate the video
                video_path, audio_path = generate_video(
                    script_urdu=proj.get('script_urdu', ''),
                    title_urdu=proj.get('title_urdu', ''),
                    arabic_text=proj.get('arabic_text', ''),
                    captions=proj.get('captions', []),
                    voice=proj.get('voice', 'ur-PK-AsadNeural'),
                    arabic_voice=proj.get('arabic_voice', 'ar-SA-HamedNeural'),
                    voice_speed=proj.get('voice_speed', '-15%'),
                    urdu_pitch=proj.get('urdu_pitch', '-10Hz'),
                    arabic_pitch=proj.get('arabic_pitch', '-5Hz'),
                    include_arabic_recitation=proj.get('include_arabic_recitation', True),
                    output_name=output_name,
                    text_effect=proj.get('text_effect', 'fade'),
                    tts_provider=proj.get('tts_provider', 'edge'),
                    resolution=proj.get('resolution', '1080p'),
                    custom_audio_path=uploaded_audio_path if use_uploaded_audio else None,
                    bg_mode=proj.get('bg_mode', 'scenery'),  # Category scenery by default
                    content_category=proj.get('content_category', 'halal'),  # Content category
                    background_audio=proj.get('background_audio', None),  # Background ASMR sound
                    background_volume=proj.get('background_volume', 0.3),  # Background volume
                    auto_generate_images=proj.get('auto_generate_images', False),  # AI images
                    image_style=proj.get('image_style', 'cinematic'),  # Image style
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

        # Show tips
        st.markdown("---")
        st.markdown("**💡 Tips:**")
        missing = [k for k, v in checks.items() if not v]
        if missing:
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
