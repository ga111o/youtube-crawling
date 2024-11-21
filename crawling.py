from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.chrome.service import Service
import unidecode
from slugify import slugify


def get_total_youtube_comments(url, i):
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=600,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    time.sleep(5)

    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    last_height = driver.execute_script(
        "return document.documentElement.scrollHeight")

    while True:
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.3)

        new_height = driver.execute_script(
            "return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(3)

    title_element = driver.find_element(
        By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[1]/h1/yt-formatted-string")
    title = title_element.text
    print("title:", title)

    comments = driver.find_elements(By.XPATH, "//*[@id='content-text']")
    authors = driver.find_elements(By.XPATH, "//*[@id='author-text']")
    votes = driver.find_elements(By.XPATH, "//*[@id='vote-count-middle']")
    written_times = driver.find_elements(
        By.XPATH, "//*[@id='published-time-text']")

    data = []
    for author, comment, vote, written_time in zip(authors, comments, votes, written_times):
        data.append({
            'URL': url,
            'Author': author.text,
            'Comment': comment.text,
            'Votes': vote.text,
            'WrittenTime': written_time.text
        })
    import re

    df = pd.DataFrame(data)

    clean_title = unidecode.unidecode(title)

    clean_title = slugify(clean_title, separator="_")

    df.to_csv(f'./{clean_title}.csv', index=False)

    driver.quit()

    print("\n")
    print("="*20)
    print("done")
    print("="*20)

    return 1


df = pd.read_csv('./links1.csv')
print(df)

for i, url in enumerate(df['URL']):
    try:
        if "shorts" in url:
            url = url.replace("shorts/", "watch?v=")
        print("===", i, url)
        get_total_youtube_comments(url, i)
    except Exception as e:
        print("====errr ", e)
