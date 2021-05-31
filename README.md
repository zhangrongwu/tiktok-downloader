# TikTok Downloader

TikTok Downloader is a Python script that allows you to download the whole tiktoks of a tiktok profile, or just a video using it's public link. It doesn't clear the watermark. You have to install dependencies from ``requirements.txt``, and the chromium binary engine on your computer. If you're a hacker, you can change the selenium configuration in ``package/downloader.py`` to use geckodriver or else.

# Sample :
This is a sample code that downloads whole video from ``tiktokfunnyhub`` into ``download/`` folder. **It must be created before running the script.**

```py
from package import downloader

def main(username: str, save_path: str):
    if username.startswith("@"):
        username = username[1:]

    downloader.download_profile(username, save_path)

if __name__ == "__main__":
    main("tiktokfunnyhub", "download/")
```

<br>

This is a sample code that downloads only one video from ``https://www.tiktok.com/@tiktokfunnyhub/video/6896204283503463685`` into ``download/`` folder. **It must be created before running the script.**

```py
from package import downloader

def main(video_url: str, save_path: str):
    downloader.download(video_url, save_path)

if __name__ == "__main__":
    main("https://www.tiktok.com/@tiktokfunnyhub/video/6896204283503463685", "download/")
```

# Misc
That's my first true Python package. I don't really know the structure I have to get to create an importable package from repo, but I think a ``git clone`` should do the work. Bye. :)