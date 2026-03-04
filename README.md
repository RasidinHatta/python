# Media & Math Processing Suite

A comprehensive, command-line utility suite written in Python that provides intuitive tools for downloading and manipulating media (video and audio), alongside an educational math testing module. 

## 🎯 MVP Project Definition

**Minimum Viable Product (MVP) Scope:**
The MVP for the **Media & Math Processing Suite** is defined as a terminal-based (CLI) application providing a unified interface to a diverse set of independent Python utilities. The core objective is to deliver functional, reliable scripts that solve everyday digital tasks without requiring heavy graphical interfaces. 

The MVP includes:
1. **Media Acquisition:** Ability to download videos and extract audio from YouTube.
2. **Media Manipulation:** Core editing features for local files including trimming videos, adjusting framerates, changing resolutions, and modifying audio properties (bitrate/sample rate).
3. **Educational Tools:** A foundational math skill-testing program to demonstrate the suite's extensibility beyond just media processing.
4. **Unified Access:** A central `main.py` entry point with an interactive, categorized menu system connecting all individual modules seamlessly.

Subsequent versions beyond the MVP could introduce graphical user interfaces (GUIs), batch processing capabilities, or web-based dashboards.

---

## 🚀 Quick Start

Run the entire suite from the central menu:

```bash
python main.py
```

This will launch the interactive **Media & Math Processing Suite** menu, where you can navigate through the Video, Audio, and Math sub-menus.

---

## 📦 Modules & Features

### 1. 📹 Video Processing Toolkit (`video_programs/`)
A collection of scripts for managing and modifying video files.

- **YouTube Downloader (`youtube2mp4.py`)**: Download videos or entire playlists from YouTube. Select from various quality metrics (144p to 4k).
- **Video Trimmer (`video_cutter.py`)**: Precisely cut sections out of video files using timecodes (HH:MM:SS or SS). High-quality output via `libx264`.
- **FPS Converter (`video_framer.py`)**: Adjust frame rates of existing videos (e.g., to 20, 24, 30, or 60 FPS) for size optimization or cinematic effects.
- **Resolution Changer (`video_enhancer.py`)**: Change video resolution and scaling. Features standard presets (480p, 720p, 1080p, 2K, 4K) while optionally preserving aspect ratios.

### 2. 🎧 Audio Processing Toolkit (`audio_programs/`)
Utilities explicitly designed for audio extraction and manipulation.

- **YouTube to MP3 Converter (`youtube2mp3.py`)**: Quickly fetch YouTube videos and extract their audio directly into MP3 format.
- **Audio Converter (`audio_converter.py`)**: Manipulate local audio files by changing their bitrate (quality), sample rate, or attempting to compress them to targeted file sizes.

### 3. 🧮 Math Programs (`math_programs/`)
Educational CLI programs for testing numerical skills.

- **Power of 5 - Math Skill Test (`math_skill_test.py`)**: A focused quiz program to test calculation speed and proficiency.

---

## 🛠 Installation & Setup

### Prerequisites

1. **Python 3.6+**
2. **FFmpeg**: The media processing tools rely heavily on FFmpeg. It must be installed and accessible in your system's PATH.
   - **Windows**: Use [Chocolatey](https://chocolatey.org/) (`choco install ffmpeg`) or download from [ffmpeg.org](https://ffmpeg.org/download.html).
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

### Python Dependencies

To ensure all programs run successfully, install the requirements located in the distinct module directories. For example:

```bash
# Install video program dependencies
pip install -r video_programs/requirements.txt

# Install audio program dependencies
pip install -r audio_programs/requirements.txt
```

---

## 📂 Directory Structure

```text
├── main.py                     # Central menu and entry point
├── README.md                   # Project documentation
├── video_programs/             # Video utilities
│   ├── youtube2mp4.py
│   ├── video_cutter.py
│   ├── video_framer.py
│   ├── video_enhancer.py
│   └── requirements.txt
├── audio_programs/             # Audio utilities
│   ├── youtube2mp3.py
│   ├── audio_converter.py
│   └── requirements.txt
└── math_programs/              # Math utilities
    └── math_skill_test.py
```

## 📜 License

MIT License
