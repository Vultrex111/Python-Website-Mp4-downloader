import os
import requests
import re
import html
import subprocess
from datetime import datetime
import random
import string

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the HTML content: {e}")
        return None

def find_m3u8_links(html_content):
    m3u8_link_pattern = re.compile(r'https:\\/\\/[^"]+\.m3u8[^"]*')
    m3u8_links = m3u8_link_pattern.findall(html_content)
    return m3u8_links

def format_link(link):
    return html.unescape(link).replace('\\/', '/')

def get_resolution_from_link(link):
    resolutions = ['1080P', '720P', '480P', '240P']
    for resolution in resolutions:
        if resolution in link:
            return resolution
    return 'Unknown'

def generate_random_string(length=8):
    characters = string.ascii_uppercase + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

def get_output_filename(resolution):
    current_date = datetime.now().strftime("%Y-%m-%d")
    random_string = generate_random_string()
    return f"{current_date}-{resolution}-{random_string}"

def download_m3u8(url, output_dir):
    resolution = get_resolution_from_link(url)
    output_filename = get_output_filename(resolution)
    try:
        subprocess.run(['yt-dlp', '-o', os.path.join(output_dir, f'{output_filename}.%(ext)s'), url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading the m3u8 link: {e}")

def main():
    url = input("Enter the URL of the webpage: ")
    output_dir = "Ph.Downloads"
    os.makedirs(output_dir, exist_ok=True)
    
    html_content = fetch_html(url)
    
    if html_content:
        m3u8_links = find_m3u8_links(html_content)
        
        if m3u8_links:
            print("Found .m3u8 links:")
            for idx, link in enumerate(m3u8_links, 1):
                formatted_link = format_link(link)
                resolution = get_resolution_from_link(formatted_link)
                print(f"{idx}: {formatted_link} ({resolution})")
            
            choice = int(input(f"Enter the number of the link to download (1-{len(m3u8_links)}): "))
            
            if 1 <= choice <= len(m3u8_links):
                selected_link = format_link(m3u8_links[choice - 1])
                print(f"Downloading {selected_link}...")
                download_m3u8(selected_link, output_dir)
                print("Download complete.")
            else:
                print("Invalid choice.")
        else:
            print("No .m3u8 links found.")
    else:
        print("Failed to fetch HTML content.")

if __name__ == '__main__':
    main()
