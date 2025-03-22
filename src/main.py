import yt_dlp
import os
import time


def get_youtube_link():
    link = input("Enter the YouTube video URL (0 to exit): ")
    return link


def get_download_type():
    print("\nWhat would you like to download?")
    print("1. Video (no conversion, progressive stream)")
    print("2. Video (conversion needed, FFmpeg required - best quality merged)")
    print("3. Audio only (no conversion, native formats)")
    print("4. Audio only (convert to MP3, FFmpeg required)")
    while True:
        choice = input("Enter your choice (1-4): ")
        if choice in ['1', '2', '3', '4']:
            return choice
        print("Invalid choice. Please try again.")


def choose_format(formats):
    print("\nAvailable formats:")
    for idx, fmt in enumerate(formats, 1):
        filesize = fmt.get('filesize')
        size_str = f" | Size: {round(filesize/1024/1024, 2)} MB" if filesize else ""
        if fmt.get('vcodec', 'none') != 'none':
            print(f"{idx}. {fmt['ext'].upper()} - {fmt['resolution']} - vcodec: {fmt['vcodec']}, acodec: {fmt['acodec']}{size_str}")
        else:
            print(f"{idx}. {fmt['ext'].upper()} - Audio bitrate: {fmt.get('abr', 'unknown')} - acodec: {fmt['acodec']}{size_str}")
    while True:
        choice = input("Select format by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(formats):
            return formats[int(choice) - 1]['format_id']
        print("Invalid selection. Please try again.")

def video_conversion(info, ydl_opts):
    formats = [f for f in info['formats'] if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('filesize')]
    if not formats:
        print("No progressive video formats found.")
        return False
    format_id = choose_format(formats)
    print(f"Downloading selected video format (no conversion)...")
    ydl_opts.update({'format': format_id})
    return True

def download_and_merge_video_audio(ydl_opts):
    print("Downloading best video and audio (merge with FFmpeg)...")
    ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            })

def download_audio(info, ydl_opts):
                formats = [f for f in info['formats'] if f.get('vcodec') == 'none' and f.get('acodec') != 'none' and f.get('filesize')]
                if not formats:
                    print("No audio formats found.")
                    return False
                format_id = choose_format(formats)
                print(f"Downloading selected audio format (no conversion)...")
                ydl_opts.update({
                    'format': format_id,
                    'postprocessors': []
                })
                return True

def download_and_convert_audio(ydl_opts):
    print("Downloading best audio and converting to MP3 (FFmpeg required)...")
    ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })

def get_unique_filename(base_path, filename, ext):
    """Generate a unique filename by adding (n) if file already exists"""
    full_path = os.path.join(base_path, f"{filename}.{ext}")
    if not os.path.exists(full_path):
        return filename
    
    counter = 1
    while True:
        new_filename = f"{filename} ({counter})"
        full_path = os.path.join(base_path, f"{new_filename}.{ext}")
        if not os.path.exists(full_path):
            return new_filename
        counter += 1

def main():
    while True:
        link = get_youtube_link()
        if link == '0':
            print("Exiting program. Goodbye!")
            break

        try:
            download_type = get_download_type()
            download_path = os.path.join(os.getcwd(), "downloads")
            os.makedirs(download_path, exist_ok=True)

            # Get video info to list formats
            ydl_opts_info = {'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(link, download=False)
            
            # Get the output extension based on download type
            output_ext = "mp4"  # Default for video
            if download_type == "3":
                # For audio-only without conversion, get extension from selected format
                formats = [f for f in info['formats'] if f.get('vcodec') == 'none' and f.get('acodec') != 'none' and f.get('filesize')]
                if formats:
                    # Will be set properly after format selection
                    output_ext = "audio"  # Placeholder
            elif download_type == "4":
                # Audio with conversion to MP3
                output_ext = "mp3"
                
            # Get custom filename
            default_title = info.get('title', 'download')
            custom_name = input(f"Enter filename (or press Enter for default '{default_title}'): ").strip()
            filename = custom_name if custom_name else default_title
            
            # Set basic options
            ydl_opts = {
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            }

            if download_type == '1':
                # Video (no conversion)
                video_conversion(info, ydl_opts)

            elif download_type == '2':
                # Video (conversion needed, best separate streams merged)
                download_and_merge_video_audio(ydl_opts)

            elif download_type == '3':
                # Audio only (no conversion)
                if download_audio(info, ydl_opts):
                    # Update output_ext with the actual extension after format selection
                    selected_format = next((f for f in info['formats'] 
                                        if f.get('format_id') == ydl_opts.get('format')), None)
                    if selected_format:
                        output_ext = selected_format.get('ext', 'audio')

            elif download_type == '4':
                # Audio only (with conversion)
                download_and_convert_audio(ydl_opts)

            # Apply unique filename
            unique_filename = get_unique_filename(download_path, filename, output_ext)
            ydl_opts['outtmpl'] = os.path.join(download_path, f"{unique_filename}.%(ext)s")

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
                print(f"Download complete! File saved as '{unique_filename}.{output_ext}' in the 'downloads' folder.")
            except Exception as e:
                print(f"Error during download: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

        input("Press Enter to continue...")
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

if __name__ == "__main__":
    main()
