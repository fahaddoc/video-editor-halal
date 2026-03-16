#!/usr/bin/env python3
"""
Halal Video Generator
=====================
Automated Islamic content video generator for YouTube

Features:
- Pre-built Islamic story scripts
- Automatic voice generation (Edge TTS - FREE)
- Video creation with backgrounds
- Easy to use CLI interface

Author: Created with Claude AI
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from config import OUTPUT_DIR, ASSETS_DIR, PEXELS_API_KEY
from src.script_generator import (
    get_categories,
    get_scripts_by_category,
    generate_custom_prompt,
    save_script,
    ISLAMIC_STORIES,
)
from src.voice_generator import generate_voice, list_available_voices
from src.stock_footage import (
    PexelsDownloader,
    create_fallback_backgrounds,
    download_footage_for_script,
)
from src.video_creator import VideoCreator, create_thumbnail

console = Console()


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner():
    """Display application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║          🌙 HALAL VIDEO GENERATOR 🌙                     ║
    ║                                                           ║
    ║     Automated Islamic Content Creator for YouTube         ║
    ║                                                           ║
    ║         ▸ Script Generation                               ║
    ║         ▸ Voice Over (FREE - Edge TTS)                    ║
    ║         ▸ Video Creation                                  ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def show_main_menu():
    """Display main menu"""
    table = Table(title="Main Menu", show_header=False, border_style="cyan")
    table.add_column("Option", style="bold yellow")
    table.add_column("Description", style="white")

    table.add_row("1", "Generate Complete Video (Automatic)")
    table.add_row("2", "Browse Scripts by Category")
    table.add_row("3", "Generate Voice Only")
    table.add_row("4", "Create Video from Existing Audio")
    table.add_row("5", "Get Custom Topic Prompt (for ChatGPT)")
    table.add_row("6", "Settings")
    table.add_row("0", "Exit")

    console.print(table)
    return Prompt.ask("\n[bold cyan]Select option[/]", choices=["0", "1", "2", "3", "4", "5", "6"])


def browse_scripts():
    """Browse available scripts by category"""
    clear_screen()
    console.print("\n[bold cyan]📚 Script Categories[/]\n")

    categories = get_categories()
    for key, name in categories.items():
        console.print(f"  [{key}] {name}")

    console.print(f"  [0] Back to Main Menu")

    choice = Prompt.ask("\n[bold]Select category[/]", choices=["0", "1", "2", "3", "4", "5"])

    if choice == "0":
        return None

    scripts = get_scripts_by_category(choice)

    if not scripts:
        console.print("[red]No scripts found in this category.[/]")
        return None

    console.print(f"\n[bold green]Available Scripts:[/]\n")
    for i, script in enumerate(scripts, 1):
        console.print(f"  [{i}] {script['title']}")

    script_choice = Prompt.ask(
        "\n[bold]Select script number[/]",
        choices=[str(i) for i in range(1, len(scripts) + 1)]
    )

    selected = scripts[int(script_choice) - 1]

    # Show preview
    console.print(Panel(
        selected['script'][:500] + "...",
        title=f"[bold]{selected['title']}[/]",
        border_style="green"
    ))

    return selected


def generate_complete_video():
    """Generate a complete video automatically"""
    clear_screen()
    console.print("\n[bold cyan]🎬 Complete Video Generation[/]\n")

    # Step 1: Select script
    console.print("[bold]Step 1: Select Script[/]")
    console.print("─" * 40)

    categories = get_categories()
    for key, name in categories.items():
        console.print(f"  [{key}] {name}")

    cat_choice = Prompt.ask("\n[bold]Category[/]", choices=["1", "2", "3", "4", "5"])
    scripts = get_scripts_by_category(cat_choice)

    if not scripts:
        console.print("[red]No scripts available.[/]")
        return

    console.print(f"\n[bold green]Scripts:[/]")
    for i, script in enumerate(scripts, 1):
        console.print(f"  [{i}] {script['title']}")

    script_choice = Prompt.ask(
        "\n[bold]Select script[/]",
        choices=[str(i) for i in range(1, len(scripts) + 1)]
    )
    selected_script = scripts[int(script_choice) - 1]

    # Step 2: Select voice
    console.print("\n[bold]Step 2: Select Voice[/]")
    console.print("─" * 40)

    voices = list_available_voices()
    for key, (voice_id, name) in voices.items():
        console.print(f"  [{key}] {name}")

    voice_choice = Prompt.ask(
        "\n[bold]Voice[/]",
        choices=list(voices.keys()),
        default="1"
    )
    voice_key = voices[voice_choice][0]

    # Step 3: Confirm and generate
    console.print("\n[bold]Step 3: Confirmation[/]")
    console.print("─" * 40)
    console.print(f"  Script: [green]{selected_script['title']}[/]")
    console.print(f"  Voice:  [green]{voices[voice_choice][1]}[/]")

    if not Confirm.ask("\n[bold]Start generation?[/]"):
        return

    # Generate!
    console.print("\n[bold yellow]⏳ Generating video...[/]\n")

    try:
        # Save script
        script_path = save_script(
            selected_script['title'],
            selected_script['script'],
            OUTPUT_DIR
        )
        console.print(f"  ✓ Script saved: {script_path.name}")

        # Generate voice
        console.print("  ⏳ Generating voiceover...")
        audio_filename = selected_script['title'].lower().replace(" ", "_") + ".mp3"
        audio_path = OUTPUT_DIR / audio_filename
        generate_voice(
            selected_script['script'],
            output_path=audio_path,
            voice=voice_key
        )
        console.print(f"  ✓ Voiceover created: {audio_path.name}")

        # Create backgrounds
        console.print("  ⏳ Creating backgrounds...")
        if PEXELS_API_KEY:
            downloader = PexelsDownloader()
            backgrounds = download_footage_for_script(cat_choice, downloader, 5)
        else:
            backgrounds = create_fallback_backgrounds(ASSETS_DIR, 5)

        if backgrounds:
            console.print(f"  ✓ Created {len(backgrounds)} backgrounds")
        else:
            backgrounds = create_fallback_backgrounds(ASSETS_DIR, 5)
            console.print(f"  ✓ Created {len(backgrounds)} fallback backgrounds")

        # Create video
        console.print("  ⏳ Creating video...")
        video_filename = selected_script['title'].lower().replace(" ", "_") + ".mp4"
        video_path = OUTPUT_DIR / video_filename

        creator = VideoCreator()
        creator.create_video_from_audio_and_images(
            audio_path=audio_path,
            image_paths=backgrounds,
            output_path=video_path,
            title=selected_script['title'],
        )
        console.print(f"  ✓ Video created: {video_path.name}")

        # Create thumbnail
        console.print("  ⏳ Creating thumbnail...")
        thumb_path = OUTPUT_DIR / f"thumb_{video_filename.replace('.mp4', '.png')}"
        create_thumbnail(selected_script['title'], thumb_path)
        console.print(f"  ✓ Thumbnail created: {thumb_path.name}")

        # Success!
        console.print("\n" + "═" * 50)
        console.print("[bold green]✅ VIDEO GENERATED SUCCESSFULLY![/]")
        console.print("═" * 50)
        console.print(f"\n📁 Output folder: [cyan]{OUTPUT_DIR}[/]")
        console.print(f"🎬 Video: [cyan]{video_path.name}[/]")
        console.print(f"🖼️  Thumbnail: [cyan]{thumb_path.name}[/]")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/]")
        import traceback
        traceback.print_exc()

    Prompt.ask("\n[dim]Press Enter to continue[/]")


def generate_voice_only():
    """Generate voice from selected script"""
    clear_screen()
    console.print("\n[bold cyan]🎙️ Voice Generation[/]\n")

    selected = browse_scripts()
    if not selected:
        return

    voices = list_available_voices()
    console.print("\n[bold]Available Voices:[/]")
    for key, (voice_id, name) in voices.items():
        console.print(f"  [{key}] {name}")

    voice_choice = Prompt.ask("\n[bold]Select voice[/]", choices=list(voices.keys()), default="1")
    voice_key = voices[voice_choice][0]

    console.print("\n[yellow]⏳ Generating voice...[/]")

    try:
        audio_filename = selected['title'].lower().replace(" ", "_") + ".mp3"
        audio_path = OUTPUT_DIR / audio_filename

        generate_voice(
            selected['script'],
            output_path=audio_path,
            voice=voice_key
        )

        console.print(f"\n[green]✅ Voice generated: {audio_path}[/]")

    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/]")

    Prompt.ask("\n[dim]Press Enter to continue[/]")


def get_custom_prompt():
    """Generate prompt for custom topic"""
    clear_screen()
    console.print("\n[bold cyan]📝 Custom Topic Prompt Generator[/]\n")

    topic = Prompt.ask("[bold]Enter your topic[/]")
    duration = Prompt.ask("[bold]Video duration (minutes)[/]", default="6")

    prompt = generate_custom_prompt(topic, int(duration))

    console.print("\n[bold green]Copy this prompt to ChatGPT:[/]")
    console.print("─" * 50)
    console.print(Panel(prompt, border_style="green"))
    console.print("─" * 50)

    console.print("\n[dim]After getting the script from ChatGPT, paste it when generating voice.[/]")

    Prompt.ask("\n[dim]Press Enter to continue[/]")


def create_video_from_audio():
    """Create video from existing audio file"""
    clear_screen()
    console.print("\n[bold cyan]🎬 Create Video from Audio[/]\n")

    # List audio files in output
    audio_files = list(OUTPUT_DIR.glob("*.mp3"))

    if not audio_files:
        console.print("[yellow]No audio files found in output folder.[/]")
        console.print(f"[dim]Place .mp3 files in: {OUTPUT_DIR}[/]")
        Prompt.ask("\n[dim]Press Enter to continue[/]")
        return

    console.print("[bold]Available audio files:[/]")
    for i, f in enumerate(audio_files, 1):
        console.print(f"  [{i}] {f.name}")

    choice = Prompt.ask(
        "\n[bold]Select audio[/]",
        choices=[str(i) for i in range(1, len(audio_files) + 1)]
    )

    audio_path = audio_files[int(choice) - 1]
    title = Prompt.ask("[bold]Video title[/]", default=audio_path.stem)

    console.print("\n[yellow]⏳ Creating video...[/]")

    try:
        # Create backgrounds
        backgrounds = create_fallback_backgrounds(ASSETS_DIR, 5)

        # Create video
        video_path = OUTPUT_DIR / f"{audio_path.stem}.mp4"
        creator = VideoCreator()
        creator.create_video_from_audio_and_images(
            audio_path=audio_path,
            image_paths=backgrounds,
            output_path=video_path,
            title=title,
        )

        console.print(f"\n[green]✅ Video created: {video_path}[/]")

    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/]")

    Prompt.ask("\n[dim]Press Enter to continue[/]")


def show_settings():
    """Show and configure settings"""
    clear_screen()
    console.print("\n[bold cyan]⚙️ Settings[/]\n")

    table = Table(show_header=True, border_style="cyan")
    table.add_column("Setting", style="bold")
    table.add_column("Value", style="green")

    table.add_row("Output Directory", str(OUTPUT_DIR))
    table.add_row("Assets Directory", str(ASSETS_DIR))
    table.add_row("Pexels API Key", "✓ Set" if PEXELS_API_KEY else "✗ Not set (using fallback)")

    console.print(table)

    console.print("\n[bold yellow]To set Pexels API key:[/]")
    console.print("  1. Go to: https://www.pexels.com/api/")
    console.print("  2. Create free account and get API key")
    console.print("  3. Set environment variable: export PEXELS_API_KEY=your_key")
    console.print("\n[dim]Note: Pexels API is optional. Without it, simple backgrounds are used.[/]")

    Prompt.ask("\n[dim]Press Enter to continue[/]")


def main():
    """Main application loop"""
    while True:
        clear_screen()
        show_banner()
        choice = show_main_menu()

        if choice == "0":
            console.print("\n[bold cyan]Allah Hafiz! 🌙[/]\n")
            sys.exit(0)
        elif choice == "1":
            generate_complete_video()
        elif choice == "2":
            selected = browse_scripts()
            if selected:
                console.print(Panel(
                    selected['script'],
                    title=f"[bold]{selected['title']}[/]",
                    border_style="green"
                ))
                Prompt.ask("\n[dim]Press Enter to continue[/]")
        elif choice == "3":
            generate_voice_only()
        elif choice == "4":
            create_video_from_audio()
        elif choice == "5":
            get_custom_prompt()
        elif choice == "6":
            show_settings()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold cyan]Allah Hafiz! 🌙[/]\n")
        sys.exit(0)
