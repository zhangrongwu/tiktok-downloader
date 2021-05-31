from package import downloader

def main(username: str, save_path: str):
    if username.startswith("@"):
        username = username[1:]

    downloader.download_profile(username, save_path)

if __name__ == "__main__":
    main("username", "destination/")