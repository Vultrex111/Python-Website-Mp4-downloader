import os
import yt_dlp

link = input("Enter the link: ")

folder_name = "RG Files"
os.makedirs(folder_name, exist_ok=True)

output_dir = os.path.join(os.getcwd(), folder_name)

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mkv',
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])
