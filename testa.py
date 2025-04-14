import time

import yt_dlp
import os
import sys

class YoutubeDownloader:

    DOWNLOAD_DIR = 'downloads'

    @classmethod
    def initialize(cls):
        if not os.path.isdir(cls.DOWNLOAD_DIR):
            os.mkdir(cls.DOWNLOAD_DIR)

    @staticmethod
    def get_file_path(url, extension):
        # Generate a filename based on the video title
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info['title']
            filename = f"{video_title}.{extension}"
            return os.path.join(YoutubeDownloader.DOWNLOAD_DIR, filename)

    @staticmethod
    def download_music_by_name(song_name):
        search_url = f"ytsearch:{song_name}"  # Search query URL for YouTube

        ydl_opts = {
            'format': 'bestaudio/best',  # Download the best audio format
            'outtmpl': '%(title)s.%(ext)s',  # Save the file with the title of the video
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=True)  # Download the first result
            if 'entries' in info:
                video = info['entries'][0]  # Get the first video in the search result
                filename = f"{video['title']}.{video['ext']}"
                print(f"Downloaded: {filename}")
                return filename
            else:
                print("No results found.")
                return None


# Command-line execution
if __name__ == "__main__":
    start_time = time.time()
    song_name = "this is ealon musk"
    YoutubeDownloader.initialize()
    downloaded_file = YoutubeDownloader.download_music_by_name(song_name)
    if downloaded_file:
        print(f"Music downloaded: {downloaded_file}")
    else:
        print("Failed to download the song.")
    end_time = time.time()

    # Calculate the time elapsed
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.4f} seconds")
