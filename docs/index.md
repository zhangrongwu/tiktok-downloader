# TikTok Downloader

### \_\_init\_\_(_self_, _chromedriver_path_: __str__)
chromedriver\_path: __str__ → Represents the absolute path to the chromedriver Selenium will have to use.

<br>

### check\_profile\_exists(_self_, _profile_: __str__) → __bool__
profile: __str__ → Represents the TikTok profile you want to check the existance.

<br>

### download(_self_, _video\_url_: __str__, _output_: __str__) → __bool__
video\_url: __str__ → Represents the TikTok source video to download.
output: __str__ → Represents the path + filename where the TikTok source video will be downloaded.

<br>

### download\_profile(_self_, _profile_: __str__, _save\_path_: __str__) → __None__
profile: __str__ → Represents the TikTok profile you want to download the content.
save\_path: __str__ → Represents the path where all the TikTok source videos will be downloaded.
