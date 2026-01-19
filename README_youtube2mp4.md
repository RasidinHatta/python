# YouTube to MP4 Downloader

A powerful Python script to download YouTube videos in all available resolutions as MP4 files.

## Features

✨ **Key Features:**
- Download videos in any available resolution (144p to 4K/8K)
- Download ALL resolutions at once
- Automatic conversion to MP4 format
- Progress tracking with speed and ETA
- List all available formats before downloading
- Custom output directory support
- Download by specific format ID

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install yt-dlp
```

### 2. Install FFmpeg (Required for format conversion)

**Windows:**
- Download from: https://ffmpeg.org/download.html
- Or use chocolatey: `choco install ffmpeg`
- Or use winget: `winget install ffmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
```

## Usage

### Interactive Mode (Easiest!)

Simply run the program without any arguments:
```bash
python youtube2mp4.py
```

The program will guide you through:
1. Entering the YouTube URL
2. Choosing whether to list formats first
3. Selecting the resolution (or downloading all)
4. Specifying the output directory

**Example Interactive Session:**
```
================================================================================
                  YouTube Video Downloader - Interactive Mode
================================================================================

Enter YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Do you want to see available formats first? (y/n, default: n): n

Available resolution options:
  - best (default) - Best available quality
  - all - Download ALL available resolutions
  - 2160p, 1440p, 1080p, 720p, 480p, 360p, 240p, 144p
  - Or enter a specific format ID

Enter resolution (press Enter for 'best'): 1080p

Enter output directory (press Enter for 'downloads'): 

Downloading...
```

### Command-Line Mode

### Basic Usage

Download in best quality:
```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download Specific Resolution

```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=VIDEO_ID" -r 1080p
```

Available resolutions: `144p`, `240p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `2160p`, `best`, `worst`

### Download All Resolutions

```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=VIDEO_ID" -r all
```

This will download the video in every available resolution!

### List Available Formats

```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=VIDEO_ID" --list
```

### Custom Output Directory

```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=VIDEO_ID" -o "./my_videos"
```

### Download by Format ID

First, list formats to see IDs:
```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=VIDEO_ID" --list
```

Then download specific format:
```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=VIDEO_ID" -f 137
```

## Command-Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `url` | - | YouTube video URL (required) |
| `--resolution` | `-r` | Resolution to download (default: best) |
| `--output` | `-o` | Output directory (default: downloads) |
| `--format-id` | `-f` | Specific format ID to download |
| `--list` | `-l` | List all available formats |

## Examples

### Example 1: Download Best Quality
```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Example 2: Download 720p
```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -r 720p
```

### Example 3: Download All Resolutions
```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -r all
```

### Example 4: Custom Directory
```bash
python youtube2mp4.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o "C:\Videos\YouTube"
```

## Output

Downloaded videos are saved with the following naming format:
```
{Video_Title}_{Resolution}.mp4
```

For example:
```
Amazing_Video_1080p.mp4
Amazing_Video_720p.mp4
Amazing_Video_480p.mp4
```

## Troubleshooting

### "yt-dlp is not installed"
Run: `pip install yt-dlp`

### "FFmpeg not found"
Install FFmpeg (see Installation section above)

### Download fails
- Check your internet connection
- Verify the YouTube URL is correct
- Some videos may be region-locked or age-restricted
- Try updating yt-dlp: `pip install --upgrade yt-dlp`

### Slow downloads
- Your internet speed affects download speed
- YouTube may throttle downloads during peak hours
- Try downloading at different times

## Notes

- **Legal Notice**: Only download videos you have permission to download
- **Quality**: Higher resolutions require more storage space
- **Speed**: Download speed depends on your internet connection
- **Formats**: The script automatically merges video and audio streams for best quality

## Advanced Usage

### Use as a Python Module

```python
from youtube2mp4 import YouTubeDownloader

# Initialize downloader
downloader = YouTubeDownloader(output_dir="my_videos")

# Download in 1080p
downloader.download_video(
    url="https://www.youtube.com/watch?v=VIDEO_ID",
    resolution="1080p"
)

# Download all resolutions
downloader.download_all_resolutions(
    url="https://www.youtube.com/watch?v=VIDEO_ID"
)

# Get available formats
formats, title = downloader.get_available_formats(
    url="https://www.youtube.com/watch?v=VIDEO_ID"
)
downloader.display_formats(formats, title)
```

## License

This script is provided as-is for educational purposes.

## Credits

Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A youtube-dl fork with additional features and fixes.
