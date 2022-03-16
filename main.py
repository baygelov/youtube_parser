import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
PATH = r"D:\Рабочий стол\youtube_parser\chromedriver\chromedriver.exe"
s = Service(executable_path=PATH)

driver = webdriver.Chrome(service=s, options=options)

name_link = []
videos = []
playlist_result = []

url = "https://www.youtube.com/c/PythonToday/playlists"

try:
    driver.get(url=url)
    playlist_titles = driver.find_elements(By.ID, "video-title")
    print(playlist_titles)

    links = []

    count = 0
    for playlist_title in playlist_titles:
        titles = [playlist_title.get_attribute('title') for playlist_title in playlist_titles]
        links = [playlist_link.get_attribute('href') for playlist_link in playlist_titles]

        name_link.append(
            {
                "Playlist name": titles[count],
                "Playlist link": links[count],
            }
        )
        count += 1

    playlist_videos = []

    count = 0
    for link in links:
        driver.get(url=link)

        driver.implicitly_wait(3)
        video_title_tags = driver.find_elements(By.ID, "video-title")
        video_titles = [video_title_tag.get_attribute('title') for video_title_tag in video_title_tags]

        driver.implicitly_wait(3)
        video_link_tags = driver.find_elements(By.ID, "wc-endpoint")
        video_links = [video_link_tag.get_attribute("href") for video_link_tag in video_link_tags]

        playlist_videos_dict = dict(zip(video_titles, video_links))
        playlist_videos.append(playlist_videos_dict)
        videos.append(
            {
                "Playlist videos": playlist_videos[count]
            }
        )
        driver.back()
        count += 1

    for i in range(0, len(name_link)):
        playlist_result.append({**name_link[i], **videos[i]})

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()

with open("play_list_result.json", "a", encoding="utf-8") as file:
    json.dump(playlist_result, file, indent=4, ensure_ascii=False)
