import sys
import os

# Add video_programs directory to sys.path so we can import the scripts
sys.path.append(os.path.join(os.path.dirname(__file__), 'video_programs'))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    # Ensure output directory exists
    if not os.path.exists('videos'):
        os.makedirs('videos')
        
    while True:
        clear_screen()
        print("=" * 60)
        print("        VIDEO PROCESSING TOOLKIT - MAIN INTERFACE")
        print("=" * 60)
        print("\nSelect a tool to run:")
        print("  1. 📺 YouTube Video Downloader")
        print("  2. ✂️  Video Trimmer (Cutter)")
        print("  3. 🎞️  FPS Converter (Frame Rate)")
        print("  4. 📐 Resolution Changer (Enhancer)")
        print("  5. ❌ Exit")
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
                print("\nGoodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")
            
            input("\nPress Enter to return to main menu...")
            
        except ImportError as e:
            print(f"\n❌ Error: Could not load the tool. {e}")
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()
