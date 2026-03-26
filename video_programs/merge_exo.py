import os

def merge_exo_files(target_dir, output_file):
    print(f"Scanning directory: {target_dir}")
    # Get all .exo files
    exo_files = [f for f in os.listdir(target_dir) if f.endswith('.exo')]
    
    if not exo_files:
        print("No .exo files found.")
        return

    # Sort files by their chunk index (the first number in the filename)
    exo_files.sort(key=lambda x: int(x.split('.')[0]))
    
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

if __name__ == "__main__":
    movie_dir = r"c:\Users\USER\Desktop\dev\python\movie"
    output_path = r"c:\Users\USER\Desktop\dev\python\merged.mp4"
    merge_exo_files(movie_dir, output_path)
