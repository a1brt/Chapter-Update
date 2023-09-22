from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time

def get_latest_chapter(driver, series_name):
    element = driver.find_element(By.PARTIAL_LINK_TEXT, series_name)
    return element.text.rsplit(' ', 1)[1]

def main():
    start = time.time()
    file_path = "latest-updates.json"
    link = "https://tcbscans.com/?date=22-9-2023-13"

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')

    with webdriver.Chrome(options=options) as driver:
        driver.get(link)

        latest_chapters = {
            'mha': get_latest_chapter(driver, "My Hero"),
            'jjk': get_latest_chapter(driver, "Jujutsu "),
            'op': get_latest_chapter(driver, "One Piece")
        }

    with open(file_path, 'r', encoding='utf-8') as json_file:
        chapters = json.load(json_file)

    updated = False
    for name, chapter in latest_chapters.items():
        if chapter != chapters.get(name):
            chapters[name] = chapter
            updated = True

    if updated:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(chapters, json_file)
    end = time.time()
    print(end -start)

if __name__ == "__main__":
    main()
