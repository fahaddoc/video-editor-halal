"""
Voice Generator Module
Uses Microsoft Edge TTS (FREE) for high-quality voice synthesis
"""
import asyncio
import edge_tts
from pathlib import Path
from config import VOICE_SETTINGS, OUTPUT_DIR


async def generate_voice_async(
    text: str,
    output_path: Path,
    voice: str = "urdu_male",
    rate: str = "-5%",
    pitch: str = "+0Hz"
) -> Path:
    """
    Generate voice from text using Edge TTS

    Args:
        text: The script text to convert to speech
        output_path: Where to save the audio file
        voice: Voice key from VOICE_SETTINGS
        rate: Speech rate (e.g., "-10%", "+10%")
        pitch: Voice pitch adjustment

    Returns:
        Path to the generated audio file
    """
    voice_id = VOICE_SETTINGS.get(voice, VOICE_SETTINGS["urdu_male"])

    communicate = edge_tts.Communicate(
        text=text,
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

    Args:
        text: The script text to convert to speech
        output_path: Where to save (default: output/voiceover.mp3)
        voice: Voice key from settings
        rate: Speech rate
        pitch: Voice pitch

    Returns:
        Path to the generated audio file
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "voiceover.mp3"

    # Clean the text
    clean_text = clean_script_for_voice(text)

    # Run async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            generate_voice_async(clean_text, output_path, voice, rate, pitch)
        )
    finally:
        loop.close()

    return result


def clean_script_for_voice(text: str) -> str:
    """
    Clean script text for better voice synthesis
    Removes stage directions, keeps spoken content
    """
    lines = text.strip().split('\n')
    clean_lines = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip stage directions in brackets
        if line.startswith('[') and line.endswith(']'):
            continue

        # Skip section headers
        if line.startswith('TITLE:') or line.startswith('==='):
            continue

        # Remove inline brackets (music cues, etc.)
        import re
        line = re.sub(r'\[.*?\]', '', line)

        # Clean up extra spaces
        line = ' '.join(line.split())

        if line:
            clean_lines.append(line)

    return '\n'.join(clean_lines)


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


async def list_all_edge_voices():
    """List all available Edge TTS voices"""
    voices = await edge_tts.list_voices()
    return voices


if __name__ == "__main__":
    # Test voice generation
    test_text = """
    Assalam o Alaikum.
    Yeh ek test hai voice generation ka.
    Umeed hai aapko pasand aayega.
    """

    output = generate_voice(test_text, voice="urdu_male")
    print(f"Voice generated: {output}")
