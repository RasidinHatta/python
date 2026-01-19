from moviepy.video.io.VideoFileClip import VideoFileClip
import os


def convert_fps(input_path, output_path, target_fps):
    """
    Convert video to specified frame rate (fps)
    """
    print(f"\nLoading video: {input_path}")
    
    # Load the video
    video = VideoFileClip(input_path)
    
    print(f"Original FPS: {video.fps}")
    print(f"Video duration: {video.duration:.2f} seconds")
    print(f"Target FPS: {target_fps}")
    
    # Convert FPS
    print(f"\nConverting video to {target_fps} FPS...")
    converted_video = video.with_fps(target_fps)
    
    # Write the result
    print(f"Saving converted video to: {output_path}")
    converted_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        fps=target_fps
    )
    
    # Close the clips
    video.close()
    converted_video.close()
    
    print(f"\n✓ Video converted successfully!")
    print(f"Output saved to: {output_path}")


def main():
    print("=" * 50)
    print("VIDEO FRAME RATE CONVERTER")
    print("=" * 50)
    
    # Get input file
    while True:
        input_path = input("\nEnter input video path: ").strip().strip('"')
        if os.path.exists(input_path):
            break
        print(f"Error: File not found: {input_path}")
    
    # Get output file
    output_path = input("Enter output video path: ").strip().strip('"')
    
    # If no extension provided, use same as input
    if not os.path.splitext(output_path)[1]:
        input_ext = os.path.splitext(input_path)[1]
        output_path += input_ext
    
    # Get target FPS
    print("\nCommon frame rates:")
    print("  20 FPS - Lower frame rate")
    print("  24 FPS - Cinematic standard")
    print("  30 FPS - Standard video")
    print("  60 FPS - Smooth video")
    
    while True:
        try:
            fps_input = input("\nEnter target FPS (e.g., 20, 24, 30, 60): ").strip()
            target_fps = float(fps_input)
            
            if target_fps <= 0:
                print("Error: FPS must be greater than 0")
                continue
            
            if target_fps > 120:
                confirm = input(f"Warning: {target_fps} FPS is very high. Continue? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue
            
            break
        except ValueError:
            print("Error: Please enter a valid number")
    
    # Convert the video
    try:
        convert_fps(input_path, output_path, target_fps)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
