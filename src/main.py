import yt_dlp
import os
import time
import sys


def get_youtube_link():
    """Get a YouTube video URL from the user."""
    link = input("Enter the YouTube video URL (0 to exit): ")
    return link

def get_format_choice():
    """Get the desired format from the user."""
    print("\nChoose download format:")
    print("1. MP4 with audio")
    print("2. Audio only (MP3)")
    print("3. MKV with audio")
    
    while True:
        choice = input("Enter your choice (1-3): ")
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please try again.")



def main():
    """Main function to orchestrate the video downloading process."""
    
    time.sleep(1)
    while True:
        link = get_youtube_link()
        
        # Exit condition
        if link == '0':
            print("Exiting program. Goodbye!")
            break
            
        format_choice = get_format_choice()
        
        # Create downloads directory if it doesn't exist
        download_path = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_path, exist_ok=True)
        
        # Configure options based on user choice
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        }
        
        
        
        if format_choice == '1':
            # MP4 with audio
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            })
            print("Downloading MP4 video with audio...")
        
        elif format_choice == '2':
            # Audio only (MP3)
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
            print("Downloading audio only (MP3)...")
        
        elif format_choice == '3':
            # MKV with audio
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mkv',
            })
            print("Downloading MKV video with audio...")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            print("Download complete! Files saved to the 'downloads' folder.")
        except Exception as e:
            print(f"Error during download: {str(e)}")
        
        input("Press Enter to continue...")
        sys.clear()

        

if __name__ == "__main__":
    main()