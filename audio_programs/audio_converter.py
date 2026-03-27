#!/usr/bin/env python3
"""
Audio Converter - Change audio bitrate, sample rate, channels, and output format.
Allows fine control over output file size, quality, and compatibility.
"""

import os
import sys
import subprocess
from pathlib import Path


# ── Dependency check ──────────────────────────────────────────────────────────

def check_ffmpeg():
    """Return True if ffmpeg is available on PATH."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_pydub():
    """Import pydub or print install hint."""
    try:
        from pydub import AudioSegment  # type: ignore # noqa: F401
        return True
    except ImportError:
        return False


# ── Helpers ───────────────────────────────────────────────────────────────────

def clear_line():
    print("\r" + " " * 80 + "\r", end="", flush=True)


def human_size(path: Path) -> str:
    size = path.stat().st_size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def get_audio_info(path: Path) -> dict:
    """Use ffprobe to extract basic info about an audio file."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        str(path),
    ]
    try:
        import json
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        streams = data.get("streams", [])
        audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
        if audio_streams:
            s = audio_streams[0]
            return {
                "codec": s.get("codec_name", "unknown"),
                "sample_rate": s.get("sample_rate", "unknown"),
                "channels": s.get("channels", "unknown"),
                "bit_rate": s.get("bit_rate", "unknown"),
                "duration": float(s.get("duration", 0)),
            }
    except Exception:
        pass
    return {}


def print_info_table(info: dict, file_path: Path):
    print(f"\n  📄 File     : {file_path.name}")
    print(f"  💾 Size     : {human_size(file_path)}")
    if info:
        br = info.get("bit_rate", "?")
        br_str = f"{int(br)//1000} kbps" if str(br).isdigit() else br
        dur = info.get("duration", 0)
        dur_str = f"{int(dur)//60}m {int(dur)%60}s" if dur else "?"
        print(f"  🎵 Codec    : {info.get('codec', '?')}")
        print(f"  ⏱  Duration : {dur_str}")
        print(f"  📡 Bitrate  : {br_str}")
        print(f"  🔊 Sample   : {info.get('sample_rate', '?')} Hz")
        print(f"  📢 Channels : {info.get('channels', '?')} "
              f"({'Stereo' if info.get('channels') == 2 else 'Mono' if info.get('channels') == 1 else ''})")


# ── Conversion ────────────────────────────────────────────────────────────────

SUPPORTED_FORMATS = ["mp3", "aac", "flac", "ogg", "wav", "m4a", "opus"]

BITRATE_OPTIONS = {
    "1": "64k",
    "2": "96k",
    "3": "128k",
    "4": "160k",
    "5": "192k",
    "6": "256k",
    "7": "320k",
}

SAMPLE_RATE_OPTIONS = {
    "1": "8000",
    "2": "11025",
    "3": "22050",
    "4": "32000",
    "5": "44100",
    "6": "48000",
    "7": "96000",
}


def choose_from_menu(title: str, options: dict, default_key: str) -> str:
    """Display a numbered menu and return the chosen value."""
    print(f"\n  {title}:")
    for k, v in options.items():
        marker = " ◀ default" if k == default_key else ""
        print(f"    {k}. {v}{marker}")
    choice = input(f"\n  Enter choice [default {default_key}]: ").strip()
    if choice not in options:
        choice = default_key
    return options[choice]


def convert_audio(
    input_path: Path,
    output_path: Path,
    bitrate: str,
    sample_rate: str,
    channels: int,
) -> bool:
    """
    Use ffmpeg to convert audio with the specified parameters.
    Returns True on success.
    """
    cmd = [
        "ffmpeg",
        "-y",                       # overwrite without asking
        "-i", str(input_path),
        "-ar", sample_rate,         # sample rate
        "-ac", str(channels),       # channels
        "-b:a", bitrate,            # audio bitrate
        str(output_path),
    ]

    print(f"\n  ⚙️  Running conversion…")
    print(f"  Command: {' '.join(cmd)}\n")

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if process.stdout is not None:
            for line in process.stdout:  # type: ignore
                # Print ffmpeg progress lines (size= ... time= ...)
                if "size=" in line or "time=" in line:
                    print(f"\r  {line.strip():<76}", end="", flush=True)
        process.wait()
        print()  # newline after progress
        return process.returncode == 0
    except Exception as e:
        print(f"\n  ❌ ffmpeg error: {e}")
        return False


# ── Interactive UI ────────────────────────────────────────────────────────────

def get_input_file() -> Path:
    """Prompt user for a valid audio input file path."""
    while True:
        raw = input("\n  Enter path to audio file: ").strip().strip('"')
        p = Path(raw)
        if p.is_file():
            return p
        print(f"  ❌ File not found: {p}")
    raise AssertionError("Unreachable")


def get_output_path(input_path: Path, fmt: str) -> Path:
    """Build default output path and ask user to confirm or change."""
    default_out = input_path.with_stem(input_path.stem + "_converted").with_suffix(f".{fmt}")
    raw = input(f"\n  Output path [Enter for: {default_out}]: ").strip().strip('"')
    if raw:
        out = Path(raw)
        # If user gave a directory, auto-name the file inside it
        if out.is_dir():
            out = out / default_out.name
    else:
        out = default_out
    out.parent.mkdir(parents=True, exist_ok=True)
    return out


def run_interactive():
    """Full interactive conversion session."""
    print("\n" + "=" * 60)
    print("        🎚️  AUDIO CONVERTER")
    print("=" * 60)
    print("  Change bitrate, sample rate, channels & format")
    print("=" * 60)

    # ── Step 1: Input file
    input_path = get_input_file()
    info = get_audio_info(input_path)
    print_info_table(info, input_path)

    # ── Step 2: Output format
    print("\n  Output Format:")
    for i, fmt in enumerate(SUPPORTED_FORMATS, 1):
        print(f"    {i}. {fmt.upper()}")
    fmt_choice = input(f"\n  Enter choice [default 1 = MP3]: ").strip()
    try:
        fmt = SUPPORTED_FORMATS[int(fmt_choice) - 1]
    except (ValueError, IndexError):
        fmt = "mp3"
    print(f"  ✅ Format: {fmt.upper()}")

    # ── Step 3: Bitrate
    bitrate = choose_from_menu("Bitrate (controls quality & file size)", BITRATE_OPTIONS, "5")
    print(f"  ✅ Bitrate: {bitrate}")

    # ── Step 4: Sample rate
    sample_rate = choose_from_menu("Sample Rate (Hz)", SAMPLE_RATE_OPTIONS, "5")
    print(f"  ✅ Sample Rate: {sample_rate} Hz")

    # ── Step 5: Channels
    print("\n  Channels:")
    print("    1. Mono   (1 channel  – smaller file)")
    print("    2. Stereo (2 channels – standard)")
    ch_choice = input("\n  Enter choice [default 2 = Stereo]: ").strip()
    channels = 1 if ch_choice == "1" else 2
    print(f"  ✅ Channels: {'Mono' if channels == 1 else 'Stereo'}")

    # ── Step 6: Output path
    output_path = get_output_path(input_path, fmt)

    # ── Summary
    print("\n" + "-" * 60)
    print("  📋 Conversion Summary")
    print("-" * 60)
    print(f"  Input   : {input_path}")
    print(f"  Output  : {output_path}")
    print(f"  Format  : {fmt.upper()}")
    print(f"  Bitrate : {bitrate}")
    print(f"  Sample  : {sample_rate} Hz")
    print(f"  Channels: {'Mono' if channels == 1 else 'Stereo'}")
    print("-" * 60)

    confirm = input("\n  Proceed? (Y/n): ").strip().lower()
    if confirm == "n":
        print("\n  ❌ Conversion cancelled.")
        return

    # ── Convert
    success = convert_audio(input_path, output_path, bitrate, sample_rate, channels)

    if success:
        out_size = human_size(output_path)
        in_size  = human_size(input_path)
        print(f"\n  ✅ Conversion successful!")
        print(f"  📁 Saved to : {output_path.absolute()}")
        print(f"  📦 Size     : {in_size}  →  {out_size}")
    else:
        print("\n  ❌ Conversion failed. Check ffmpeg output above.")


# ── Main entry point ──────────────────────────────────────────────────────────

def main():
    """Entry point called from main.py menu."""
    # Dependency checks
    if not check_ffmpeg():
        print("\n  ❌ ffmpeg is not installed or not in PATH.")
        print("  👉 Download from: https://ffmpeg.org/download.html")
        print("     and add it to your system PATH.")
        input("\n  Press Enter to return to menu...")
        return

    if not check_pydub():
        print("\n  ℹ️  pydub is not installed (optional for metadata).")
        print("     pip install pydub")

    try:
        run_interactive()
    except KeyboardInterrupt:
        print("\n\n  ⚠️  Interrupted by user.")


if __name__ == "__main__":
    main()
