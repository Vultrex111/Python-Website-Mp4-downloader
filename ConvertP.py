import os
import requests
import re
import html
import subprocess
import sys
from datetime import datetime

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
    return m3u8_link_pattern.findall(html_content)

def format_link(link):
    return html.unescape(link).replace('\\/', '/')

def get_resolution_from_link(link):
    resolutions = ['1080P', '720P', '480P', '240P']
    for resolution in resolutions:
        if resolution in link:
            return resolution
    return 'Unknown'

def extract_title(html_content):
    title_pattern = re.compile(r'<title>(.*?)<\/title>', re.IGNORECASE | re.DOTALL)
    match = title_pattern.search(html_content)
    if match:
        return match.group(1).strip()
    return 'Unknown_Title'

def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '-', filename)

def get_output_filename(title, resolution):
    sanitized_title = sanitize_filename(title)
    return f"{sanitized_title}-{resolution}"

def download_m3u8(url, output_dir, title):
    resolution = get_resolution_from_link(url)
    output_filename = get_output_filename(title, resolution)
    output_path = os.path.join(output_dir, f'{output_filename}.%(ext)s')
    
    try:
        subprocess.run(['yt-dlp', '-o', output_path, url], check=True)
        print(f"Download complete: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading the m3u8 link: {e}")

def main():
    url = input("Enter the URL of the webpage: ").strip()
    output_dir = "Ph.Downloads"
    
    os.makedirs(output_dir, exist_ok=True)
    
    html_content = fetch_html(url)
    
    if not html_content:
        print("Failed to fetch HTML content.")
        return
    
    m3u8_links = find_m3u8_links(html_content)
    
    if not m3u8_links:
        print("No .m3u8 links found.")
        return
    
    title = extract_title(html_content)
    
    print("Found .m3u8 links:")
    for idx, link in enumerate(m3u8_links, 1):
        formatted_link = format_link(link)
        resolution = get_resolution_from_link(formatted_link)
        print(f"{idx}: {formatted_link} ({resolution})")
    
    try:
        choice = int(input(f"Enter the number of the link to download (1-{len(m3u8_links)}): "))
        if not 1 <= choice <= len(m3u8_links):
            raise ValueError("Choice out of range.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return
    
    selected_link = format_link(m3u8_links[choice - 1])
    print(f"Downloading {selected_link}...")
    download_m3u8(selected_link, output_dir, title)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
        sys.exit(0)
