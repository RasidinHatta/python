#!/usr/bin/env python3
"""
YouTube Video Downloader - Download videos in all available resolutions
Supports downloading individual videos or entire playlists in MP4 format
"""

import os
import sys
import argparse
from pathlib import Path
try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Please install it using: pip install yt-dlp")
    sys.exit(1)


class YouTubeDownloader:
    """YouTube video downloader with support for multiple resolutions"""
    
    def __init__(self, output_dir="downloads"):
        """
        Initialize the downloader
        
        Args:
            output_dir: Directory where videos will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_available_formats(self, url):
        """
        Get all available video formats for a given URL
        
        Args:
            url: YouTube video URL
            
        Returns:
            List of available formats with details
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                # Filter for video formats with both video and audio or video only
                video_formats = []
                for f in formats:
                    if f.get('vcodec') != 'none':  # Has video
                        video_formats.append({
                            'format_id': f.get('format_id'),
                            'ext': f.get('ext'),
                            'resolution': f.get('resolution', 'audio only'),
                            'fps': f.get('fps', 'N/A'),
                            'vcodec': f.get('vcodec', 'none'),
                            'acodec': f.get('acodec', 'none'),
                            'filesize': f.get('filesize', 'Unknown'),
                            'format_note': f.get('format_note', ''),
                        })
                
                return video_formats, info.get('title', 'Unknown')
        except Exception as e:
            print(f"Error getting formats: {e}")
            return [], None
    
    def display_formats(self, formats, title):
        """
        Display available formats in a readable format
        
        Args:
            formats: List of format dictionaries
            title: Video title
        """
        print(f"\n{'='*80}")
        print(f"Video: {title}")
        print(f"{'='*80}")
        print(f"{'ID':<10} {'Resolution':<15} {'FPS':<8} {'Codec':<15} {'Audio':<10} {'Size':<15}")
        print(f"{'-'*80}")
        
        for fmt in formats:
            size = fmt['filesize']
            if isinstance(size, int):
                size = f"{size / (1024*1024):.2f} MB"
            else:
                size = "Unknown"
            
            print(f"{fmt['format_id']:<10} {fmt['resolution']:<15} {str(fmt['fps']):<8} "
                  f"{fmt['vcodec'][:15]:<15} {fmt['acodec'][:10]:<10} {size:<15}")
    
    def download_video(self, url, resolution="best", format_id=None):
        """
        Download a video in specified resolution
        
        Args:
            url: YouTube video URL
            resolution: Resolution to download (e.g., '1080p', '720p', 'best', 'all')
            format_id: Specific format ID to download
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if resolution == "all":
                return self.download_all_resolutions(url)
            
            # Configure download options
            ydl_opts = {
                'outtmpl': str(self.output_dir / '%(title)s_%(resolution)s.%(ext)s'),
                'format': self._get_format_string(resolution, format_id),
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'progress_hooks': [self._progress_hook],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"\nDownloading video in {resolution}...")
                ydl.download([url])
                print("\n✓ Download completed successfully!")
                return True
                
        except Exception as e:
            print(f"\n✗ Error downloading video: {e}")
            return False
    
    def download_all_resolutions(self, url):
        """
        Download video in all available resolutions
        
        Args:
            url: YouTube video URL
            
        Returns:
            True if all downloads successful, False otherwise
        """
        formats, title = self.get_available_formats(url)
        
        if not formats:
            print("No formats found!")
            return False
        
        # Get unique resolutions (filter out duplicates)
        unique_resolutions = {}
        for fmt in formats:
            res = fmt['resolution']
            if res != 'audio only' and res not in unique_resolutions:
                # Prefer formats with audio
                if fmt['acodec'] != 'none':
                    unique_resolutions[res] = fmt['format_id']
        
        print(f"\nFound {len(unique_resolutions)} unique video resolutions")
        print(f"Downloading all resolutions for: {title}\n")
        
        success_count = 0
        for i, (res, fmt_id) in enumerate(unique_resolutions.items(), 1):
            print(f"\n[{i}/{len(unique_resolutions)}] Downloading {res}...")
            
            ydl_opts = {
                'outtmpl': str(self.output_dir / f'%(title)s_{res}.%(ext)s'),
                'format': f'{fmt_id}+bestaudio/best',
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'progress_hooks': [self._progress_hook],
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    success_count += 1
                    print(f"✓ {res} completed")
            except Exception as e:
                print(f"✗ Failed to download {res}: {e}")
        
        print(f"\n{'='*80}")
        print(f"Download Summary: {success_count}/{len(unique_resolutions)} successful")
        print(f"{'='*80}")
        
        return success_count == len(unique_resolutions)
    
    def _get_format_string(self, resolution, format_id=None):
        """
        Get the format string for yt-dlp based on resolution
        
        Args:
            resolution: Desired resolution
            format_id: Specific format ID
            
        Returns:
            Format string for yt-dlp
        """
        if format_id:
            return f'{format_id}+bestaudio/best'
        
        resolution_map = {
            'best': 'bestvideo+bestaudio/best',
            'worst': 'worstvideo+worstaudio/worst',
            '2160p': 'bestvideo[height<=2160]+bestaudio/best',
            '1440p': 'bestvideo[height<=1440]+bestaudio/best',
            '1080p': 'bestvideo[height<=1080]+bestaudio/best',
            '720p': 'bestvideo[height<=720]+bestaudio/best',
            '480p': 'bestvideo[height<=480]+bestaudio/best',
            '360p': 'bestvideo[height<=360]+bestaudio/best',
            '240p': 'bestvideo[height<=240]+bestaudio/best',
            '144p': 'bestvideo[height<=144]+bestaudio/best',
        }
        
        return resolution_map.get(resolution.lower(), 'bestvideo+bestaudio/best')
    
    def _progress_hook(self, d):
        """
        Progress hook for download status
        
        Args:
            d: Dictionary containing download progress information
        """
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"\rProgress: {percent} | Speed: {speed} | ETA: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\rDownload finished, now converting...", end='', flush=True)


def get_user_input():
    """
    Get user input interactively
    
    Returns:
        Dictionary with user choices
    """
    print(f"\n{'='*80}")
    print(f"{'YouTube Video Downloader - Interactive Mode':^80}")
    print(f"{'='*80}\n")
    
    # Get URL
    while True:
        url = input("Enter YouTube URL: ").strip()
        if url:
            break
        print("❌ URL cannot be empty. Please try again.\n")
    
    # Ask if user wants to list formats first
    list_formats = input("\nDo you want to see available formats first? (y/n, default: n): ").strip().lower()
    
    if list_formats == 'y':
        return {'url': url, 'list': True, 'resolution': None, 'output': 'downloads', 'format_id': None}
    
    # Get resolution
    print("\nAvailable resolution options:")
    print("  - best (default) - Best available quality")
    print("  - all - Download ALL available resolutions")
    print("  - 2160p, 1440p, 1080p, 720p, 480p, 360p, 240p, 144p")
    print("  - Or enter a specific format ID")
    
    resolution = input("\nEnter resolution (press Enter for 'best'): ").strip()
    if not resolution:
        resolution = 'best'
    
    # Get output directory
    output = input("\nEnter output directory (press Enter for 'downloads'): ").strip()
    if not output:
        output = 'downloads'
    
    return {
        'url': url,
        'list': False,
        'resolution': resolution,
        'output': output,
        'format_id': None
    }


def main():
    """Main function to handle command-line interface"""
    parser = argparse.ArgumentParser(
        description='Download YouTube videos in various resolutions as MP4',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (no arguments)
  python youtube2mp4.py
  
  # Download in best quality
  python youtube2mp4.py https://www.youtube.com/watch?v=VIDEO_ID
  
  # Download in specific resolution
  python youtube2mp4.py https://www.youtube.com/watch?v=VIDEO_ID -r 1080p
  
  # Download all available resolutions
  python youtube2mp4.py https://www.youtube.com/watch?v=VIDEO_ID -r all
  
  # List available formats
  python youtube2mp4.py https://www.youtube.com/watch?v=VIDEO_ID --list
  
  # Download to specific directory
  python youtube2mp4.py https://www.youtube.com/watch?v=VIDEO_ID -o ./my_videos
  
  # Download using specific format ID
  python youtube2mp4.py https://www.youtube.com/watch?v=VIDEO_ID -f 137
        """
    )
    
    parser.add_argument('url', nargs='?', help='YouTube video URL (optional - will prompt if not provided)')
    parser.add_argument('-r', '--resolution', 
                       default='best',
                       help='Resolution to download (e.g., 1080p, 720p, best, all). Default: best')
    parser.add_argument('-o', '--output', 
                       default='downloads',
                       help='Output directory. Default: downloads')
    parser.add_argument('-f', '--format-id',
                       help='Specific format ID to download')
    parser.add_argument('-l', '--list',
                       action='store_true',
                       help='List all available formats and exit')
    
    args = parser.parse_args()
    
    # If no URL provided, enter interactive mode
    if not args.url:
        user_input = get_user_input()
        args.url = user_input['url']
        args.list = user_input['list']
        args.resolution = user_input['resolution'] or args.resolution
        args.output = user_input['output']
        args.format_id = user_input['format_id']
    
    # Initialize downloader
    downloader = YouTubeDownloader(output_dir=args.output)
    
    # List formats if requested
    if args.list:
        formats, title = downloader.get_available_formats(args.url)
        if formats:
            downloader.display_formats(formats, title)
        else:
            print("Could not retrieve formats for this video.")
        return
    
    # Download video
    print(f"\n{'='*80}")
    print(f"YouTube Video Downloader")
    print(f"{'='*80}")
    print(f"URL: {args.url}")
    print(f"Resolution: {args.resolution}")
    print(f"Output Directory: {args.output}")
    print(f"{'='*80}\n")
    
    success = downloader.download_video(
        url=args.url,
        resolution=args.resolution,
        format_id=args.format_id
    )
    
    if success:
        print(f"\n✓ All downloads saved to: {downloader.output_dir.absolute()}")
    else:
        print(f"\n✗ Download failed or incomplete")
        sys.exit(1)


if __name__ == "__main__":
    main()
