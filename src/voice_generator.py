"""
Voice Generator Module
Uses Microsoft Edge TTS (FREE) for high-quality voice synthesis
"""
import asyncio
import re
import edge_tts
from pathlib import Path
from config import VOICE_SETTINGS, OUTPUT_DIR


def clean_script_for_voice(text: str) -> str:
    """
    Clean script text for better voice synthesis
    Removes stage directions, keeps only spoken content
    """
    lines = text.strip().split('\n')
    clean_lines = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip lines that are entirely in brackets (stage directions)
        if line.startswith('[') and line.endswith(']'):
            continue

        # Skip section headers and markers
        if line.startswith('TITLE:') or line.startswith('==='):
            continue

        # Skip pure formatting lines
        if line.startswith('---') or line.startswith('***'):
            continue

        # Remove inline brackets (music cues, stage directions)
        line = re.sub(r'\[.*?\]', '', line)

        # Remove asterisks (markdown bold/italic)
        line = line.replace('*', '')

        # Remove hashtags
        line = re.sub(r'#\w+', '', line)

        # Clean up multiple spaces
        line = ' '.join(line.split())

        # Skip if line is now empty or too short
        if len(line) < 2:
            continue

        clean_lines.append(line)

    # Join with proper pauses
    result = '\n'.join(clean_lines)

    # Add natural pauses
    result = result.replace('...', ', ')  # Convert ellipsis to pause
    result = result.replace('؟', '?')  # Urdu question mark
    result = result.replace('۔', '.')  # Urdu period

    return result


def get_spoken_lines(text: str) -> list:
    """
    Extract individual spoken lines for subtitle display
    """
    clean_text = clean_script_for_voice(text)
    lines = []

    for line in clean_text.split('\n'):
        line = line.strip()
        if line and len(line) > 2:
            # Split long lines
            if len(line) > 80:
                # Split at sentence boundaries
                sentences = re.split(r'(?<=[.!?])\s+', line)
                for sent in sentences:
                    if sent.strip():
                        lines.append(sent.strip())
            else:
                lines.append(line)

    return lines


async def generate_voice_async(
    text: str,
    output_path: Path,
    voice: str = "urdu_male",
    rate: str = "-5%",
    pitch: str = "+0Hz"
) -> Path:
    """
    Generate voice from text using Edge TTS
    """
    voice_id = VOICE_SETTINGS.get(voice, VOICE_SETTINGS["urdu_male"])

    # Clean the text
    clean_text = clean_script_for_voice(text)

    communicate = edge_tts.Communicate(
        text=clean_text,
        voice=voice_id,
        rate=rate,
        pitch=pitch
    )

    await communicate.save(str(output_path))
    return output_path


def generate_voice(
    text: str,
    output_path: Path = None,
    voice: str = "urdu_male",
    rate: str = "-5%",
    pitch: str = "+0Hz"
) -> Path:
    """
    Synchronous wrapper for voice generation
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "voiceover.mp3"

    # Run async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            generate_voice_async(text, output_path, voice, rate, pitch)
        )
    finally:
        loop.close()

    return result


def list_available_voices():
    """Return available voice options"""
    return {
        "1": ("urdu_male", "Urdu - Male (Asad)"),
        "2": ("urdu_female", "Urdu - Female (Uzma)"),
        "3": ("hindi_male", "Hindi - Male (Madhur)"),
        "4": ("hindi_female", "Hindi - Female (Swara)"),
        "5": ("english_male", "English - Male (Guy)"),
        "6": ("english_female", "English - Female (Jenny)"),
        "7": ("arabic_male", "Arabic - Male (Hamed)"),
        "8": ("arabic_female", "Arabic - Female (Zariyah)"),
    }


if __name__ == "__main__":
    test_text = """
    Assalam o Alaikum.
    Yeh ek test hai voice generation ka.
    """
    output = generate_voice(test_text, voice="urdu_male")
    print(f"Voice generated: {output}")
