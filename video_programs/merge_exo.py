import os
import shutil
import subprocess
import tempfile

def get_exo_sort_key(filename):
    parts = filename.split(".")
    numbers = []

    for part in parts:
        if part.isdigit():
            numbers.append(int(part))

    # ExoPlayer cache files are usually named:
    #   content_id.position.last_touch_timestamp.v3.exo
    # The position is the byte offset and is the safest merge order.
    if len(numbers) >= 2:
        return (numbers[0], numbers[1], filename)

    return (0, numbers[0] if numbers else 0, filename)

def get_exo_files(target_dir):
    print(f"Scanning directory: {target_dir}")

    exo_files = [f for f in os.listdir(target_dir) if f.lower().endswith('.exo')]

    if not exo_files:
        print("No .exo files found.")
        return []

    exo_files.sort(key=get_exo_sort_key)
    return exo_files

def get_subtitle_file(target_dir):
    subtitle_files = [f for f in os.listdir(target_dir) if f.lower().endswith(".en")]

    if not subtitle_files:
        return None

    subtitle_files.sort()
    subtitle_path = os.path.join(target_dir, subtitle_files[0])
    print(f"Found subtitle file: {subtitle_path}")
    return subtitle_path

def merge_exo_files(target_dir, output_file, exo_files=None):
    if exo_files is None:
        exo_files = get_exo_files(target_dir)

    if not exo_files:
        return False
    
    print(f"Found {len(exo_files)} .exo files. Merging into {output_file}...")
    
    # Merge them into a single file
    with open(output_file, 'wb') as outfile:
        for idx, fname in enumerate(exo_files):
            fpath = os.path.join(target_dir, fname)
            with open(fpath, 'rb') as infile:
                outfile.write(infile.read())
                
            if (idx + 1) % 50 == 0:
                print(f"Merged {idx + 1} / {len(exo_files)} files...")
                
    print(f"\nSuccessfully merged all files into: {output_file}")
    return True

def build_ffmpeg_mp4_args(ffmpeg_path, input_args, output_file, subtitle_file=None):
    args = [ffmpeg_path, "-y"] + input_args

    if subtitle_file:
        args += [
            "-f",
            "srt",
            "-i",
            subtitle_file,
            "-map",
            "0",
            "-map",
            "1",
            "-c",
            "copy",
            "-c:s",
            "mov_text",
            "-metadata:s:s:0",
            "language=eng",
            output_file,
        ]
    else:
        args += ["-c", "copy", output_file]

    return args

def create_mp4_with_ffmpeg(target_dir, output_file, exo_files, subtitle_file=None):
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        print("\nffmpeg is required to create a playable .mp4 file from .exo chunks.")
        print("Install ffmpeg and run this script again.")
        return False

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as concat_file:
        concat_path = concat_file.name
        for fname in exo_files:
            fpath = os.path.abspath(os.path.join(target_dir, fname)).replace("\\", "/")
            concat_file.write(f"file '{fpath}'\n")

    try:
        print(f"\nCreating MP4 video: {output_file}")
        subprocess.run(
            build_ffmpeg_mp4_args(
                ffmpeg_path,
                [
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    concat_path,
                ],
                output_file,
                subtitle_file,
            ),
            check=True,
        )
        print(f"\nSuccessfully created MP4 file: {output_file}")
        return True
    except subprocess.CalledProcessError:
        print("\nDirect ffmpeg concat failed. Trying raw merge + MP4 remux...")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".exo") as temp_file:
            temp_path = temp_file.name

        try:
            if not merge_exo_files(target_dir, temp_path, exo_files):
                return False

            subprocess.run(
                build_ffmpeg_mp4_args(
                    ffmpeg_path,
                    ["-i", temp_path],
                    output_file,
                    subtitle_file,
                ),
                check=True,
            )
            print(f"\nSuccessfully created MP4 file: {output_file}")
            return True
        except subprocess.CalledProcessError:
            print("\nffmpeg could not create the MP4 file.")
            print("The .exo files may be encrypted, incomplete, or from separate audio/video streams.")
            return False
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    finally:
        if os.path.exists(concat_path):
            os.remove(concat_path)

def main():
    print("\n--- Merge .exo Video Files ---")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    movie_dir = os.path.join(project_dir, "movie")
    
    output_filename = input("Enter output file name (e.g., merged.mp4) [Default: merged.mp4]: ").strip()
    if not output_filename:
        output_filename = "merged.mp4"
    
    if not output_filename.lower().endswith(".mp4"):
        output_filename += ".mp4"
        
    output_path = os.path.join(movie_dir, output_filename)
    exo_files = get_exo_files(movie_dir)
    subtitle_file = get_subtitle_file(movie_dir)

    if exo_files:
        create_mp4_with_ffmpeg(movie_dir, output_path, exo_files, subtitle_file)

if __name__ == "__main__":
    main()
