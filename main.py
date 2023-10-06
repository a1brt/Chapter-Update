from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notification import notify
from mongodb import get_chapters, update_latest_chapter
import time

INTERVAL_IN_SECONDS = 120

def get_latest_chapter(driver, series_name, chapter):
    try:
        element = driver.find_element(By.PARTIAL_LINK_TEXT, series_name)
        return element.text.rsplit(' ', 1)[1]
    except Exception as ex:
        print(ex)
        return chapter

def main():
    start = time.time()
    link = "https://tcbscans.com/"

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')
    chapters = get_chapters()

    with webdriver.Chrome(options=options) as driver:
        driver.get(link)

        latest_chapters = {
            'MHA': get_latest_chapter(driver, "My Hero", chapters["MHA"]),
            'JJK': get_latest_chapter(driver, "Jujutsu", chapters["JJK"]),
            'OP': get_latest_chapter(driver, "One Piece", chapters["OP"])
        }

    for name, chapter in latest_chapters.items():
        if chapter != chapters.get(name):
            update_latest_chapter(name, chapter)
            notify(name,chapter)

    end = time.time()
    print(f"{time.strftime('%H:%M:%S', time.localtime())}: {end - start}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(INTERVAL_IN_SECONDS)
