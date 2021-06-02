from context import TikTok_Downloader

def main(profile: str, save_path: str):
    if profile.startswith("@"):
        profile = profile[1:]
    tiktok_downloader = TikTok_Downloader("../drivers/win.exe")
    tiktok_downloader.download_profile(profile, save_path)


if __name__ == "__main__":
    main("username", "destination/")
