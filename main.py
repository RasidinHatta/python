import sys
import os

# Add video_programs and audio_programs directories to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'video_programs'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'audio_programs'))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def video_menu():
    # Ensure output directory exists
    if not os.path.exists('videos'):
        os.makedirs('videos')
        
    while True:
        clear_screen()
        print("=" * 60)
        print("        VIDEO PROCESSING TOOLKIT")
        print("=" * 60)
        print("\nSelect a tool to run:")
        print("  1. 📺 YouTube Video Downloader")
        print("  2. ✂️  Video Trimmer (Cutter)")
        print("  3. 🎞️  FPS Converter (Frame Rate)")
        print("  4. 📐 Resolution Changer (Enhancer)")
        print("  5. 🔙 Return to Main Menu")
        print("\n" + "=" * 60)
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        try:
            if choice == '1':
                import youtube2mp4
                youtube2mp4.main()
            elif choice == '2':
                import video_cutter
                video_cutter.main()
            elif choice == '3':
                import video_framer
                video_framer.main()
            elif choice == '4':
                import video_enhancer
                video_enhancer.main()
            elif choice == '5':
                break
            else:
                print("\nInvalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
            
        except ImportError as e:
            print(f"\n❌ Error: Could not load the tool. {e}")
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            input("\nPress Enter to continue...")

def audio_menu():
    # Ensure output directory exists
    if not os.path.exists('audio'):
        os.makedirs('audio')
        
    while True:
        clear_screen()
        print("=" * 60)
        print("        AUDIO PROCESSING TOOLKIT")
        print("=" * 60)
        print("\nSelect a tool to run:")
        print("  1. 🎵 YouTube to MP3 Converter")
        print("  2. 🔙 Return to Main Menu")
        print("\n" + "=" * 60)
        
        choice = input("\nEnter choice (1-2): ").strip()
        
        try:
            if choice == '1':
                import youtube2mp3
                youtube2mp3.main()
            elif choice == '2':
                break
            else:
                print("\nInvalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
            
        except ImportError as e:
            print(f"\n❌ Error: Could not load the tool. {e}")
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            input("\nPress Enter to continue...")

def main_menu():
    while True:
        clear_screen()
        print("=" * 60)
        print("        MEDIA PROCESSING SUITE")
        print("=" * 60)
        print("\nSelect program type:")
        print("  1. 📹 Video Programs")
        print("  2. 🎧 Audio Programs")
        print("  3. ❌ Exit")
        print("\n" + "=" * 60)
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            video_menu()
        elif choice == '2':
            audio_menu()
        elif choice == '3':
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()
