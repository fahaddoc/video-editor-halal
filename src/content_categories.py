"""
Content Categories System
Different themes, sceneries, and styles for various content types
"""

CONTENT_CATEGORIES = {
    # ===== ISLAMIC/HALAL =====
    "halal": {
        "name": "🕌 Islamic / Halal",
        "description": "Islamic educational content, Hadith, Quran, duas",
        "scenery": "islamic_village",
        "color_scheme": {
            "primary": (255, 215, 0),      # Gold
            "secondary": (30, 60, 100),     # Deep blue
            "accent": (100, 200, 150),      # Soft green
            "text": (255, 255, 255),
            "bg_start": (5, 15, 35),
            "bg_end": (20, 40, 80),
        },
        "mood": "peaceful",
        "voices": {
            "urdu": "ur-PK-AsadNeural",
            "arabic": "ar-SA-HamedNeural",
            "english": "en-US-GuyNeural",
        },
        "music_style": "nasheed",
        "elements": ["mosque", "moon", "stars", "minaret", "lantern"],
    },

    # ===== HORROR =====
    "horror": {
        "name": "👻 Horror Stories",
        "description": "Scary stories, paranormal, suspense",
        "scenery": "horror_night",
        "color_scheme": {
            "primary": (180, 0, 0),          # Blood red
            "secondary": (20, 20, 30),       # Dark
            "accent": (100, 0, 50),          # Dark purple
            "text": (200, 200, 200),
            "bg_start": (5, 5, 10),
            "bg_end": (15, 10, 20),
        },
        "mood": "scary",
        "voices": {
            "urdu": "ur-PK-AsadNeural",
            "english": "en-US-GuyNeural",
        },
        "music_style": "suspense",
        "elements": ["dead_tree", "abandoned_house", "fog", "bats", "graveyard"],
    },

    # ===== MYSTERY/CRIME =====
    "mystery": {
        "name": "🔍 Murder Mystery",
        "description": "Crime stories, detective, thriller",
        "scenery": "noir_city",
        "color_scheme": {
            "primary": (200, 50, 50),        # Red accent
            "secondary": (30, 30, 40),       # Dark grey
            "accent": (255, 200, 100),       # Yellow light
            "text": (255, 255, 255),
            "bg_start": (10, 10, 15),
            "bg_end": (25, 25, 35),
        },
        "mood": "suspenseful",
        "voices": {
            "urdu": "ur-PK-AsadNeural",
            "english": "en-US-GuyNeural",
        },
        "music_style": "noir",
        "elements": ["city_building", "streetlight", "rain", "car_silhouette"],
    },

    # ===== KIDS EDUCATIONAL =====
    "kids": {
        "name": "🧒 Kids / Educational",
        "description": "Children's content, learning, fun facts",
        "scenery": "sunny_village",
        "color_scheme": {
            "primary": (255, 150, 50),       # Orange
            "secondary": (100, 200, 255),    # Sky blue
            "accent": (255, 100, 150),       # Pink
            "text": (50, 50, 80),
            "bg_start": (135, 200, 255),
            "bg_end": (200, 230, 255),
        },
        "mood": "cheerful",
        "voices": {
            "urdu": "ur-PK-UzmaNeural",       # Female for kids
            "english": "en-US-JennyNeural",
        },
        "music_style": "playful",
        "elements": ["sun", "clouds", "rainbow", "cute_house", "flowers", "butterflies"],
    },

    # ===== MOTIVATIONAL =====
    "motivational": {
        "name": "💪 Motivational",
        "description": "Self-help, inspiration, success stories",
        "scenery": "sunrise_mountains",
        "color_scheme": {
            "primary": (255, 180, 50),       # Warm gold
            "secondary": (80, 60, 120),      # Purple
            "accent": (255, 100, 80),        # Coral
            "text": (255, 255, 255),
            "bg_start": (40, 30, 60),
            "bg_end": (255, 150, 100),
        },
        "mood": "inspiring",
        "voices": {
            "urdu": "ur-PK-AsadNeural",
            "english": "en-US-GuyNeural",
        },
        "music_style": "uplifting",
        "elements": ["mountains", "sun_rays", "birds", "clouds"],
    },

    # ===== HISTORY =====
    "history": {
        "name": "📜 History",
        "description": "Historical events, biographies, ancient civilizations",
        "scenery": "ancient_ruins",
        "color_scheme": {
            "primary": (180, 150, 100),      # Sepia
            "secondary": (60, 50, 40),       # Brown
            "accent": (200, 180, 140),       # Parchment
            "text": (240, 230, 210),
            "bg_start": (30, 25, 20),
            "bg_end": (60, 50, 40),
        },
        "mood": "nostalgic",
        "voices": {
            "urdu": "ur-PK-AsadNeural",
            "english": "en-GB-RyanNeural",   # British accent
        },
        "music_style": "epic",
        "elements": ["ruins", "columns", "old_building", "torch"],
    },

    # ===== SCIENCE =====
    "science": {
        "name": "🔬 Science / Tech",
        "description": "Science facts, technology, space, nature",
        "scenery": "space",
        "color_scheme": {
            "primary": (0, 200, 255),        # Cyan
            "secondary": (20, 30, 60),       # Space blue
            "accent": (150, 100, 255),       # Purple
            "text": (255, 255, 255),
            "bg_start": (5, 10, 30),
            "bg_end": (15, 25, 50),
        },
        "mood": "wonder",
        "voices": {
            "urdu": "ur-PK-AsadNeural",
            "english": "en-US-GuyNeural",
        },
        "music_style": "ambient",
        "elements": ["planets", "stars", "nebula", "satellite", "rocket"],
    },

    # ===== ROMANCE/POETRY =====
    "poetry": {
        "name": "💕 Poetry / Shayari",
        "description": "Urdu poetry, ghazals, romantic content",
        "scenery": "moonlit_garden",
        "color_scheme": {
            "primary": (255, 150, 180),      # Soft pink
            "secondary": (60, 40, 80),       # Purple
            "accent": (255, 200, 150),       # Peach
            "text": (255, 255, 255),
            "bg_start": (30, 20, 50),
            "bg_end": (60, 40, 80),
        },
        "mood": "romantic",
        "voices": {
            "urdu": "ur-PK-AsadNeural",
        },
        "music_style": "classical",
        "elements": ["moon", "rose", "fountain", "garden", "fireflies"],
    },

    # ===== NEWS/FACTS =====
    "facts": {
        "name": "📰 Facts / News",
        "description": "Interesting facts, news stories, information",
        "scenery": "minimal",
        "color_scheme": {
            "primary": (50, 150, 255),       # Blue
            "secondary": (30, 30, 40),       # Dark
            "accent": (255, 200, 50),        # Yellow highlight
            "text": (255, 255, 255),
            "bg_start": (15, 20, 35),
            "bg_end": (25, 35, 55),
        },
        "mood": "informative",
        "voices": {
            "urdu": "ur-PK-AsadNeural",
            "english": "en-US-GuyNeural",
        },
        "music_style": "news",
        "elements": ["globe", "graphs", "icons"],
    },

    # ===== GAMING =====
    "gaming": {
        "name": "🎮 Gaming",
        "description": "Gaming content, reviews, walkthroughs",
        "scenery": "cyber",
        "color_scheme": {
            "primary": (0, 255, 200),        # Neon cyan
            "secondary": (20, 10, 40),       # Dark purple
            "accent": (255, 0, 150),         # Neon pink
            "text": (255, 255, 255),
            "bg_start": (10, 5, 25),
            "bg_end": (30, 15, 50),
        },
        "mood": "energetic",
        "voices": {
            "urdu": "ur-PK-AsadNeural",
            "english": "en-US-GuyNeural",
        },
        "music_style": "electronic",
        "elements": ["neon_grid", "glitch", "particles"],
    },
}


def get_category(category_id: str) -> dict:
    """Get category configuration by ID"""
    return CONTENT_CATEGORIES.get(category_id, CONTENT_CATEGORIES["halal"])


def list_categories() -> dict:
    """List all available categories"""
    return {k: v["name"] for k, v in CONTENT_CATEGORIES.items()}


def get_category_voices(category_id: str) -> dict:
    """Get voice options for a category"""
    cat = get_category(category_id)
    return cat.get("voices", {})


def get_category_colors(category_id: str) -> dict:
    """Get color scheme for a category"""
    cat = get_category(category_id)
    return cat.get("color_scheme", {})


# Print summary
if __name__ == "__main__":
    print("Available Content Categories:")
    print("=" * 50)
    for cat_id, cat in CONTENT_CATEGORIES.items():
        print(f"\n{cat['name']}")
        print(f"  ID: {cat_id}")
        print(f"  Description: {cat['description']}")
        print(f"  Mood: {cat['mood']}")
        print(f"  Elements: {', '.join(cat['elements'][:3])}...")
