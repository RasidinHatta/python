# Video Processing Utilities

A collection of Python scripts for downloading, trimming, and adjusting video frame rates.

## Tools Included

### 1. YouTube Downloader (`youtube2mp4.py`)

A powerful script to download YouTube videos or playlists in various resolutions.

- **Features**:
  - Download individual videos or entire playlists.
  - Choose specific resolutions (144p to 4K).
  - List available formats before downloading.
  - Automatic conversion to MP4 using FFmpeg.
- **Usage**:
  ```bash
  python video_programs/youtube2mp4.py
  ```
  _(Follow the interactive prompts or use command-line arguments)_

### 2. Video Trimmer (`video_cutter.py`)

A simple utility to cut sections out of video files.

- **Features**:
  - Supports HH:MM:SS, MM:SS, or SS time formats.
  - High-quality output using libx264.
- **Usage**:
  ```bash
  python video_programs/video_cutter.py
  ```

### 3. FPS Converter (`video_framer.py`)

Adjust the frame rate of any video file.

- **Features**:
  - Convert to standard frame rates (20, 24, 30, 60 FPS).
  - Useful for reducing file size or achieving specific cinematic looks.
- **Usage**:
  ```bash
  python video_programs/video_framer.py
  ```

## Installation

### Prerequisites

- **Python 3.6+**
- **FFmpeg**: This tool must be installed on your system.
  - **Windows**: Install via [Chocolatey](https://chocolatey.org/) (`choco install ffmpeg`) or download from [ffmpeg.org](https://ffmpeg.org/download.html).
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `sudo apt install ffmpeg`

### Python Dependencies

Install the required libraries using pip:

```bash
pip install -r video_programs/requirements.txt
```

## Directory Structure

- `video_programs/`: Contains all script files and requirements.
  - `youtube2mp4.py`: YouTube downloader.
  - `video_cutter.py`: Video trimming tool.
  - `video_framer.py`: FPS conversion tool.
  - `requirements.txt`: Python package list.

## License

MIT License
