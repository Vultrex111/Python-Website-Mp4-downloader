import requests
import re
import html
import subprocess

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

def download_m3u8(url):
    try:
        subprocess.run(['yt-dlp', url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading the m3u8 link: {e}")

def main():
    url = input("Enter the URL of the webpage: ")
    html_content = fetch_html(url)
    
    if html_content:
        m3u8_links = find_m3u8_links(html_content)
        
        if m3u8_links:
            print("Found .m3u8 links:")
            for idx, link in enumerate(m3u8_links, 1):
                formatted_link = format_link(link)
                print(f"{idx}: {formatted_link}")
            
            choice = int(input(f"Enter the number of the link to download (1-{len(m3u8_links)}): "))
            
            if 1 <= choice <= len(m3u8_links):
                selected_link = format_link(m3u8_links[choice - 1])
                print(f"Downloading {selected_link}...")
                download_m3u8(selected_link)
                print("Download complete.")
            else:
                print("Invalid choice.")
        else:
            print("No .m3u8 links found.")
    else:
        print("Failed to fetch HTML content.")

if __name__ == '__main__':
    main()
