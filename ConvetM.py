import yt_dlp
import os
import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def extract_resolutions_and_links(url):
    # Create yt-dlp options
    ydl_opts = {
        'quiet': True,  # Suppress console output
        'format': 'best',  # Select best quality format
        'get-url': True,  # Get direct video URL
        'list-formats': True  # List available formats
    }

    # Create yt-dlp object
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Get video info
        info = ydl.extract_info(url, download=False)
        
        # Print available formats
        print("Available formats:")
        for i, format in enumerate(info['formats']):
            resolution = format['resolution'] if 'resolution' in format else 'Audio'
            print(f"{i + 1}. {resolution}")

        # Prompt user to select a format
        while True:
            try:
                choice = int(input("Select a format (enter the corresponding number): "))
                selected_format = info['formats'][choice - 1]
                break
            except (ValueError, IndexError):
                print("Invalid selection. Please enter a valid number.")

        # Get URL of selected format
        format_url = selected_format['url']

        # Generate random filename
        random_name = generate_random_string(5)
        output_file = f"{random_name}-video.mp4"

        # Convert .ts to .mp4 using ffmpeg directly
        os.system(f"ffmpeg -i {format_url} -c copy {output_file}")
        print(f"Video converted to .mp4 format successfully. Saved as {output_file}.")

if __name__ == "__main__":
    # Input URL from terminal
    url = input("Enter the video URL: ")
    
    # Extract resolutions and links
    extract_resolutions_and_links(url)

