import requests
import re
import subprocess

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the HTML content: {e}")
        return None

def find_mp4_links(html):
    mp4_link_pattern = re.compile(r'https?://[^"]+\.mp4')
    mp4_links = mp4_link_pattern.findall(html)
    return mp4_links

def download_video(url):
    try:
        result = subprocess.run(['aria2c', url], check=True)
        if result.returncode == 0:
            print("Download complete.")
        else:
            print("Download failed.")
    except subprocess.CalledProcessError as e:
        print(f"Error during download: {e}")

def main():
    url = input("Enter the URL of the webpage: ")
    html_content = fetch_html(url)
    
    if html_content:
        mp4_links = find_mp4_links(html_content)
        
        if mp4_links:
            print("Found .mp4 links:")
            for idx, link in enumerate(mp4_links, 1):
                print(f"{idx}: {link}")
            
            try:
                choice = int(input(f"Enter the number of the link to download (1-{len(mp4_links)}): "))
                if 1 <= choice <= len(mp4_links):
                    selected_link = mp4_links[choice - 1]
                    print(f"Downloading {selected_link}...")
                    download_video(selected_link)
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("No .mp4 links found.")
    else:
        print("Failed to fetch HTML content.")

if __name__ == '__main__':
    main()
