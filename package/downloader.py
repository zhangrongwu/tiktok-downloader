from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from json import dumps, loads
from requests import get
from os import listdir
from re import findall, match
from time import sleep
from math import pi

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "accept": "*/*",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://www.tiktok.com/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1"
}


def fetch_data(uri: str, asBytes: bool = True) -> bytes:
    req = get(uri, headers=headers)

    # Handles TikTok trackers to not get a forbidden access.
    jsonHeaders = req.headers
    for k, v in jsonHeaders.items():
        k = k.lower()
        if k == "set-cookie":
            headers["cookie"] = jsonHeaders["Set-Cookie"]
        elif k.startswith("x-"):
            headers[k[2:]] = v

    headers["referer"] = uri
    return req.content if asBytes else req.text


def get_raw_video_link(data: str) -> str:
    links = findall(r"\"downloadAddr\":\"(.*?)\"", data)
    if len(links) == 0:
        return ""

    link = links[0].replace("\\u0026", "&")
    return link


def download(video_url: str, output: str) -> bool:
    video_html = fetch_data(video_url, False)

    rawVideoLink = get_raw_video_link(video_html)
    if not rawVideoLink:
        print("No rawVideoLink, exiting.")
        return

    video_bytes = fetch_data(rawVideoLink)
    try:
        if "Access Denied" in video_bytes.decode("utf8"):
            return False
    except:
        s = open(output, "wb+")
        s.write(video_bytes)
        s.close()
        return True


def download_profile(username: str, save_path: str, videoLinks: list = [], i: int = 0):
    debug = False
    if i == 0:
        try:
            videoLinks = loads(open("saves.json", 'r').read())
        except:
            options = Options()
            if not debug:
                options.add_argument("--headless")
                options.add_argument("--silent")
                options.add_argument("--disable-gpu")
                options.add_argument("--log-level=3")
                options.add_experimental_option(
                    'excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(options=options)
            profile = f"https://www.tiktok.com/@{username}/?is_copy_url=1&is_from_webapp=v1"
            driver.get(profile)

            if debug:
                print(f"Profile URL : {profile}")

            last_height = driver.execute_script(
                "return document.body.scrollHeight")

            while True:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")

                sleep(1)

                new_height = driver.execute_script(
                    "return document.body.scrollHeight")

                if new_height == last_height:
                    break

                last_height = new_height

            sleep(1)

            body = driver.page_source
            for href in findall(r"https:\/\/www.tiktok.com\/@\w+\/video\/\d+", body):
                if not href in videoLinks:
                    videoLinks.append(href)

            driver.quit()
            open("saves.json", "w+").write(dumps(videoLinks))

    already_saved = listdir(save_path)
    for link in videoLinks:
        videoUrl = link.replace("\\u0026", "&")
        videoName = videoUrl.split('/')[-1].split('?')[0] + ".mp4"
        if videoName in already_saved:
            continue
        elif download(videoUrl, save_path + videoName):
            i += 1

    if i < len(videoLinks):
        download_profile(username, save_path, videoLinks, i)
