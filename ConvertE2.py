import os
import re
import requests
import subprocess
from urllib.parse import urljoin


def get_mp4_links(url):
    response = requests.get(url)
    content = response.text

    mp4_links = re.findall(r'href="(.*?\.mp4).*?>(.*?)</a>', content)

    mp4_links_with_size = []
    for link, description in mp4_links:
        size_match = re.search(r'(\d+(\.\d+)?)\s*([KMGT]?B)', description)
        if size_match:
            size = size_match.group(1)
            unit = size_match.group(3)
            mp4_links_with_size.append({'link': urljoin(url, link), 'size': f"{size} {unit}"})

    return mp4_links_with_size


def display_mp4_links(mp4_links):
    print("Available MP4 links:")
    for i, link in enumerate(mp4_links, start=1):
        print(f"{i}. {link['link']} - Size: {link['size']}")


def download_selected_link(mp4_links):
    selection = int(input("Enter the number of the link you want to download: "))
    selected_link = mp4_links[selection - 1]['link']
    filename = selected_link.split('/')[-1]
    download_dir = input("Enter the directory to save the file (leave blank for current directory): ").strip()
    if download_dir:
        os.makedirs(download_dir, exist_ok=True)
        subprocess.run(['aria2c', '-d', download_dir, '-o', filename, selected_link])
        file_path = os.path.join(download_dir, filename)
    else:
        subprocess.run(['aria2c', '-o', filename, selected_link])
        file_path = filename

    # Ask the user if they want to open the video with mpv
    open_video = input("Do you want to open the video with mpv? (yes/no): ").strip().lower()
    if open_video in ['yes', 'y']:
        subprocess.run(['mpv', file_path])


def main():
    url = input("Enter the URL of the webpage: ")
    mp4_links = get_mp4_links(url)
    display_mp4_links(mp4_links)
    download_selected_link(mp4_links)


if __name__ == "__main__":
    main()

