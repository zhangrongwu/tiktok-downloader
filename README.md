# TikTok Downloader

TikTok Downloader is a Python script that allows you to download the whole tiktoks of a tiktok profile, or just a video using it's public link. It doesn't clear the watermark. You have to install dependencies from ``requirements.txt``, and the chromium binary engine on your computer.

# Sample :
This is a sample code that downloads whole video from ``USERNAME_WITHOUT_@`` into ``download/`` folder. __It must be created before running the script.__

```py
from package import downloader

def main(username: str, save_path: str):
    if username.startswith("@"):
        username = username[1:]

    downloader.download_profile(username, save_path)

if __name__ == "__main__":
    main("USERNAME_WITHOUT_@", "download/")
```

<br>

This is a sample code that downloads only one video from ``VIDEO_URL`` into ``download/`` folder. __It must be created before running the script.__

```py
from package import downloader

def main(video_url: str, save_path: str):
    downloader.download(video_url, save_path)

if __name__ == "__main__":
    main("VIDEO_URL", "download/")
```