from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from requests import get
from os import listdir
from re import findall
from time import sleep


class TikTok_Downloader:
    def __init__(self, chromedriver_path: str) -> None:
        self.__headers = {
            "user-agent": "Naverbot",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://www.tiktok.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "cross-site",
            "sec-gpc": "1"
        }
        self.__video_list = []
        self.__chromedriver_path = chromedriver_path
        return None

    def __fetch_data(self, uri: str, as_bytes: bool = True) -> bytes:
        req = get(uri, headers=self.__headers)

        # Handles TikTok trackers to not get a forbidden access.
        server_headers = req.headers
        for k, v in server_headers.items():
            k = k.lower()
            if k == "set-cookie":
                self.__headers["cookie"] = server_headers["Set-Cookie"]
            elif k.startswith("x-"):
                # Removes the "x-" before any TikTok"s header to push it into self.__headers
                self.__headers[k[2:]] = v

        self.__headers["referer"] = uri
        return req.content if as_bytes else req.text

    def __get_raw_video_link(self, data: str) -> str:
        links = findall(r"\"downloadAddr\":\"(.*?)\"", data)
        return "" if len(links) == 0 else links[0].replace("\\u0026", "&")

    def __build_driver(self, debug=False):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("user-agent="+self.__headers["user-agent"])
        # options.add_argument("--no-sandbox")
        if not debug:
            options.add_argument("--headless")
            options.add_argument("--silent")
            options.add_argument("--disable-gpu")
            options.add_argument("--log-level=3")
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return Chrome(self.__chromedriver_path, options=options)

    def check_profile_exists(self, profile: str) -> bool:
        r = get("https://www.tiktok.com/@" + profile)
        return r.status_code == 200

    def download(self, video_url: str, output: str) -> bool:
        video_html = self.__fetch_data(video_url, False)
        video_link = self.__get_raw_video_link(video_html)

        if not video_link:
            return

        video_bytes = self.__fetch_data(video_link)
        try:
            if "Access Denied" in video_bytes.decode("utf8"):
                return False
        except:
            s = open(output, "wb+")
            s.write(video_bytes)
            s.close()
            return True

    def download_profile(self, profile: str, save_path: str) -> None:
        if self.__video_list == []:
            if not self.check_profile_exists(profile):
                return

            profile = "https://www.tiktok.com/@" + \
                profile + "/?is_copy_url=1&is_from_webapp=v1"

            driver = self.__build_driver(debug=True)
            driver.get(profile)
            last_height = driver.execute_script(
                "return document.body.scrollHeight")
            height = 0
            while height <= last_height:
                print("INWHILE")
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")

                sleep(2)

                height = driver.execute_script(
                    "return document.body.scrollHeight")

                for href in findall(r"https:\/\/www\.tiktok\.com\/@\w+\/video\/\d+", driver.page_source):
                    if not href in self.__video_list:
                        self.__video_list.append(href)

                if last_height == height:
                    break

                last_height = height

            driver.quit()

        already_saved = listdir(save_path)
        for i, link in enumerate(self.__video_list):
            video_url = link.replace("\\u0026", "&")
            video_name = video_url.split("/")[-1].split("?")[0] + ".mp4"
            if video_name in already_saved:
                continue
            elif self.download(video_url, save_path + video_name):
                del self.__video_list[i]

        return self.download_profile(profile, save_path) if len(self.__video_list) > 0 else None
