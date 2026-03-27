from moviepy.video.io.VideoFileClip import VideoFileClip  # type: ignore
import os

def resize_video(input_path, output_path, width=None, height=None, res_name=None):
    """
    Resize video to specified width and/or height
    """
    print(f"\nLoading video: {input_path}")
    
    # Load the video
    video = VideoFileClip(input_path)
    
    print(f"Original Resolution: {video.w}x{video.h}")
    print(f"Video duration: {video.duration:.2f} seconds")
    
    # Perform resizing
    # Note: moviepy v2.x uses .resized(width=..., height=...)
    # If only one is provided, aspect ratio is typically preserved
    print(f"\nResizing video to {res_name if res_name else f'{width}x{height}'}...")
    
    if width and height:
        resized_video = video.resized(width=width, height=height)
    elif width:
        resized_video = video.resized(width=width)
    elif height:
        resized_video = video.resized(height=height)
    else:
        resized_video = video
        print("No resizing parameters provided, keeping original resolution.")

    print(f"New Resolution: {resized_video.w}x{resized_video.h}")
    
    # Write the result
    print(f"Saving resized video to: {output_path}")
    resized_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    # Close the clips
    video.close()
    resized_video.close()
    
    print(f"\n✓ Video resized successfully!")
    print(f"Output saved to: {output_path}")


def main():
    print("=" * 50)
    print("VIDEO RESOLUTION CHANGER (ENHANCER)")
    print("=" * 50)
    
    # Get input file
    while True:
        input_path = input("\nEnter input video path: ").strip().strip('"')
        if os.path.exists(input_path):
            break
        print(f"Error: File not found: {input_path}")
    
    # Get target Resolution
    print("\nCommon Resolutions:")
    print("  1. 4K   (3840x2160)")
    print("  2. 2K   (2560x1440)")
    print("  3. 1080p (1920x1080)")
    print("  4. 720p  (1280x720)")
    print("  5. 480p  (854x480)")
    print("  6. Custom width (preserve aspect ratio)")
    print("  7. Custom height (preserve aspect ratio)")
    print("  8. Custom width x height")
    
    choice = input("\nSelect an option (1-8): ").strip()
    
    width, height, res_name = None, None, None
    res_suffix = ""
    
    if choice == '1':
        width, height, res_name = 3840, 2160, "4K"
        res_suffix = "4k"
    elif choice == '2':
        width, height, res_name = 2560, 1440, "2K"
        res_suffix = "2k"
    elif choice == '3':
        width, height, res_name = 1920, 1080, "1080p"
        res_suffix = "1080p"
    elif choice == '4':
        width, height, res_name = 1280, 720, "720p"
        res_suffix = "720p"
    elif choice == '5':
        width, height, res_name = 854, 480, "480p"
        res_suffix = "480p"
    elif choice == '6':
        width = int(input("Enter target width: ").strip())
        res_suffix = f"{width}w"
    elif choice == '7':
        height = int(input("Enter target height: ").strip())
        res_suffix = f"{height}h"
    elif choice == '8':
        width = int(input("Enter target width: ").strip())
        height = int(input("Enter target height: ").strip())
        res_suffix = f"{width}x{height}"
    else:
        print("Invalid choice. Exiting.")
        return 1

    # Get output file suggestion
    input_filename = os.path.basename(input_path)
    name_part, ext_part = os.path.splitext(input_filename)
    default_output = os.path.join("videos", f"{name_part}_output_enhancer_{res_suffix}{ext_part}")
    
    print(f"\nSuggested output: {default_output}")
    output_path = input(f"Enter output video path (press Enter for default): ").strip().strip('"')
    
    if not output_path:
        output_path = default_output
    
    # If no extension provided, use same as input
    if not os.path.splitext(output_path)[1]:
        output_path += ext_part
    
    # Resize the video
    try:
        resize_video(input_path, output_path, width, height, res_name)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
