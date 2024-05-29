import subprocess
import re

def fetch_html(url):
    # Use wget2 to fetch the HTML content of the webpage
    result = subprocess.run(['wget2', '--quiet', '-O-', url], capture_output=True, text=True)
    return result.stdout

def find_mp4_links(html):
    # Define the regex pattern to match any .mp4 links
    mp4_link_pattern = re.compile(r'https:\/\/[^"]+\.mp4')
    
    # Find all matches in the HTML content
    mp4_links = mp4_link_pattern.findall(html)
    
    return mp4_links

def download_video(url):
    # Use aria2c to download the selected video
    subprocess.run(['aria2c', url])

def main():
    url = input("Enter the URL of the webpage: ")
    html_content = fetch_html(url)
    
    if html_content:
        mp4_links = find_mp4_links(html_content)
        
        if mp4_links:
            print("Found .mp4 links:")
            for idx, link in enumerate(mp4_links, 1):
                print(f"{idx}: {link}")
            
            # Prompt the user to choose a link to download
            choice = int(input(f"Enter the number of the link to download (1-{len(mp4_links)}): "))
            
            if 1 <= choice <= len(mp4_links):
                selected_link = mp4_links[choice - 1]
                print(f"Downloading {selected_link}...")
                download_video(selected_link)
                print("Download complete.")
            else:
                print("Invalid choice.")
        else:
            print("No .mp4 links found.")
    else:
        print("Failed to fetch HTML content.")

if __name__ == '__main__':
    main()

