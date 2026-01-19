from moviepy.video.io.VideoFileClip import VideoFileClip
import os


def parse_time(time_str):
    """
    Parse time string in format HH:MM:SS or MM:SS or SS
    Returns time in seconds
    """
    parts = time_str.strip().split(':')
    
    try:
        if len(parts) == 1:  # SS
            return float(parts[0])
        elif len(parts) == 2:  # MM:SS
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:  # HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        else:
            raise ValueError("Invalid time format")
    except ValueError:
        raise ValueError("Invalid time format. Use HH:MM:SS, MM:SS, or SS")


def trim_video(input_path, output_path, start_time, end_time):
    """
    Trim video from start_time to end_time
    """
    print(f"\nLoading video: {input_path}")
    
    # Load the video
    video = VideoFileClip(input_path)
    
    print(f"Video duration: {video.duration:.2f} seconds")
    
    # Validate times
    if start_time < 0:
        raise ValueError("Start time cannot be negative")
    
    if end_time > video.duration:
        raise ValueError(f"End time ({end_time:.2f}s) exceeds video duration ({video.duration:.2f}s)")
    
    if start_time >= end_time:
        raise ValueError("Start time must be less than end time")
    
    # Trim the video
    print(f"\nTrimming video from {start_time:.2f}s to {end_time:.2f}s...")
    trimmed_video = video.subclipped(start_time, end_time)
    
    # Write the result
    print(f"Saving trimmed video to: {output_path}")
    trimmed_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    # Close the clips
    video.close()
    trimmed_video.close()
    
    print(f"\n✓ Video trimmed successfully!")
    print(f"Output saved to: {output_path}")


def main():
    print("=" * 50)
    print("VIDEO TRIMMER")
    print("=" * 50)
    
    # Get input file
    while True:
        input_path = input("\nEnter input video path: ").strip().strip('"')
        if os.path.exists(input_path):
            break
        print(f"Error: File not found: {input_path}")
    
    # Get output file suggestion
    input_dir = os.path.dirname(input_path)
    input_filename = os.path.basename(input_path)
    name_part, ext_part = os.path.splitext(input_filename)
    default_output = os.path.join("videos", f"{name_part}_output_cutter{ext_part}")
    
    print(f"\nSuggested output: {default_output}")
    output_path = input(f"Enter output video path (press Enter for default): ").strip().strip('"')
    
    if not output_path:
        output_path = default_output
    
    # If no extension provided, use same as input
    if not os.path.splitext(output_path)[1]:
        output_path += ext_part
    
    # Get start time
    while True:
        try:
            start_time_str = input("\nEnter start time (HH:MM:SS or MM:SS or SS): ").strip()
            start_time = parse_time(start_time_str)
            break
        except ValueError as e:
            print(f"Error: {e}")
    
    # Get end time
    while True:
        try:
            end_time_str = input("Enter end time (HH:MM:SS or MM:SS or SS): ").strip()
            end_time = parse_time(end_time_str)
            break
        except ValueError as e:
            print(f"Error: {e}")
    
    # Trim the video
    try:
        trim_video(input_path, output_path, start_time, end_time)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
