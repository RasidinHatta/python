#!/usr/bin/env python3
"""
YouTube Audio Downloader - Download audio from YouTube videos in MP3 format
"""

import os
import sys
import argparse
from pathlib import Path
try:
    import yt_dlp  # type: ignore
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Please install it using: pip install yt-dlp")
    sys.exit(1)


class YouTubeAudioDownloader:
    """YouTube audio downloader"""
    
    def __init__(self, output_dir="audio"):
        """
        Initialize the downloader
        
        Args:
            output_dir: Directory where audio files will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download_audio(self, url, quality="192"):
        """
        Download audio from video
        
        Args:
            url: YouTube video URL
            quality: Audio bitrate (e.g., '192', '128', '320')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Configure download options
            ydl_opts = {
                'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                }],
                'progress_hooks': [self._progress_hook],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"\nDownloading audio (MP3 - {quality}kbps)...")
                ydl.download([url])
                print("\n✓ Download completed successfully!")
                return True
                
        except Exception as e:
            print(f"\n✗ Error downloading audio: {e}")
            return False
    
    def _progress_hook(self, d):
        """
        Progress hook for download status
        """
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"\rProgress: {percent} | Speed: {speed} | ETA: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\rDownload finished, now converting to MP3...", end='', flush=True)


def get_user_input():
    """
    Get user input interactively
    """
    print(f"\n{'='*80}")
    print(f"{'YouTube Audio Downloader - Interactive Mode':^80}")
    print(f"{'='*80}\n")
    
    # Get URL
    while True:
        url = input("Enter YouTube URL: ").strip()
        if url:
            break
        print("❌ URL cannot be empty. Please try again.\n")
    
    # Get Quality
    quality = input("\nEnter audio quality (128, 192, 320) [default: 192]: ").strip()
    if not quality or quality not in ['128', '192', '320']:
        quality = '192'
    
    # Get output directory
    output = input("\nEnter output directory (press Enter for 'audio'): ").strip()
    if not output:
        output = 'audio'
    
    return {
        'url': url,
        'quality': quality,
        'output': output
    }


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Download YouTube videos as MP3 audio',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('url', nargs='?', help='YouTube video URL')
    parser.add_argument('-q', '--quality', 
                       default='192',
                       choices=['128', '192', '320'],
                       help='Audio quality (bitrate). Default: 192')
    parser.add_argument('-o', '--output', 
                       default='audio',
                       help='Output directory. Default: audio')
    
    args = parser.parse_args()
    
    url = args.url
    quality = args.quality
    output = args.output
    
    # If no URL provided, enter interactive mode
    if not url:
        user_input = get_user_input()
        url = user_input['url']
        quality = user_input['quality']
        output = user_input['output']
    
    # Initialize downloader
    downloader = YouTubeAudioDownloader(output_dir=output)
    
    # Download audio
    print(f"\n{'='*80}")
    print(f"YouTube Audio Downloader")
    print(f"{'='*80}")
    print(f"URL: {url}")
    print(f"Quality: {quality}kbps")
    print(f"Output Directory: {output}")
    print(f"{'='*80}\n")
    
    success = downloader.download_audio(
        url=url,
        quality=quality
    )
    
    if success:
        print(f"\n✓ Audio saved to: {downloader.output_dir.absolute()}")
    else:
        print(f"\n✗ Download failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
