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
        mp4_links_with_size.append({'link': urljoin(url, link)})

    return mp4_links_with_size

def display_mp4_links(mp4_links):
    print("Available MP4 links:")
    for i, link in enumerate(mp4_links, start=1):
        print(f"{i}. {link['link']}")

def download_selected_link(mp4_links):
    selection = int(input("Enter the number of the link you want to download: "))
    selected_link = mp4_links[selection - 1]['link']
    filename = selected_link.split('/')[-1]
    download_dir = input("Enter the directory to save the file (leave blank for current directory): ").strip()
    if download_dir:
        os.makedirs(download_dir, exist_ok=True)
        subprocess.run(['wget', selected_link, '-P', download_dir])
    else:
        subprocess.run(['wget', selected_link])

def main():
    url = input("Enter the URL of the webpage: ")
    mp4_links = get_mp4_links(url)
    display_mp4_links(mp4_links)
    download_selected_link(mp4_links)

if __name__ == "__main__":
    main()

