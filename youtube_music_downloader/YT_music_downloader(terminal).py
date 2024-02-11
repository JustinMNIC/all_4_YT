from pytube import YouTube, Playlist

def download_video(url, output_path="."):
    try:
        yt = YouTube(url, allow_oauth_cache=True, use_oauth=True) ## https://github.com/pytube/pytube/issues/1712 (for context) for some reason there is an error with the age restriction, and the only way (that I could find till now) to bypass the age restriction error is by going to the dir where your interpretor is installed (inluding the pytube lib.), open " innertube.py " and in  line 223 change ANDROID_MUSIC to !!! ANDROID, IOS, IOS_EMBED, or ANDROID_CREATOR
        title = yt.title
        duration = yt.length
        print(f"Downloading: {title}")

        if duration >= 150 and "Interview" not in title:
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path)
            print(f"Finished downloading: {title}")
        else:
            print(f"Skipped: {title} (Doesn't meet requirements)")

    except Exception as e:
        print(f"Error: {e}")

def download_playlist(url, output_path="."):
    try:
        playlist = Playlist(url)
        for video_url in playlist.video_urls:
            download_video(video_url, output_path)
    except Exception as e:
        print(f"Error: {e}")
        
def download_from_txt(file_path, output_path="."):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                url = line.strip()
                if url:
                    if "&list=" in url.lower():
                        download_playlist(url, output_path)
                    elif "watch" in url.lower() and "&list=" not in url.lower():
                        download_video(url, output_path)
                    else:
                        print(f"Invalid YouTube link in the file: {url}")
    except Exception as e:
        print(f"Error reading from file: {e}")

def main():
    user_input  = input("Enter YouTube link or path to .txt document: ")
    user_input.strip('"')
    
    output_folder = input("Enter output folder (press Enter for the current folder): ") or "."
    output_folder.strip('"')
    
    if user_input.lower().endswith('.txt'):
        download_from_txt(user_input, output_folder)
    else:
        if "&list=" in user_input.lower():
            download_playlist(user_input, output_folder)
        elif "watch" in user_input.lower() and "&list=" not in user_input.lower():
            download_video(user_input, output_folder)
        else:
            print("Invalid YouTube link or file path.")
        
if __name__ == "__main__":
    main()
