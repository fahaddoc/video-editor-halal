# Halal Video Generator

Automated Islamic content video generator for YouTube. Create professional videos with voiceovers completely FREE.

## Features

- **Pre-built Scripts**: Islamic stories, Sahaba stories, Prophet stories, Quran lessons, motivational content
- **Auto Voice Generation**: Using Microsoft Edge TTS (FREE, high quality)
- **Video Creation**: Automatic video with backgrounds and titles
- **Easy to Use**: Simple command-line interface

## Requirements

- Python 3.8+
- FFmpeg

## Quick Start

### 1. Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### 2. Setup

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### 3. Run

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
```

## Usage

### Generate Complete Video

1. Select option `1` from main menu
2. Choose a category (Sahaba stories, Prophet stories, etc.)
3. Select a script
4. Choose voice (Urdu, Hindi, English, Arabic)
5. Wait for generation

Output files will be in the `output/` folder.

### Available Voices

| Language | Male | Female |
|----------|------|--------|
| Urdu | Asad | Uzma |
| Hindi | Madhur | Swara |
| English | Guy | Jenny |
| Arabic | Hamed | Zariyah |

## Optional: Pexels API

For better stock footage, get a free API key:

1. Go to [pexels.com/api](https://www.pexels.com/api/)
2. Create free account
3. Get API key
4. Set environment variable:

```bash
export PEXELS_API_KEY=your_key_here
```

Without Pexels, simple gradient backgrounds are used.

## Output Files

After generation, you'll find in `output/`:

- `video_name.mp4` - Final video
- `video_name.mp3` - Voiceover audio
- `thumb_video_name.png` - Thumbnail
- `video_name.txt` - Script text

## Custom Topics

Use option `5` to generate prompts for custom topics. Copy the prompt to ChatGPT, get the script, then use option `3` to generate voice.

## Troubleshooting

### "FFmpeg not found"
Install FFmpeg using instructions above.

### "No module named 'moviepy'"
Run: `pip install -r requirements.txt`

### Voice generation fails
Check internet connection (Edge TTS requires internet).

## License

Free to use for halal content creation.

## Credits

- Voice: Microsoft Edge TTS
- Video: MoviePy
- Stock footage: Pexels (optional)
