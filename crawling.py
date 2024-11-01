from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import csv
import pandas as pd
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.firefox.service import Service


def get_total_youtube_comments(url, i, rep_num=2):

    # options.add_argument("window-size=600,1080")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # service = Service('./geckodriver')
    # driver = webdriver.Firefox(service=service, options=options)
    # driver.get(url)

    options = webdriver.FirefoxOptions()
    options.add_argument("--width=600")
    options.add_argument("--height=1080")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument(
    #     "user-agent={Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36}")

    service = Service('./geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("url")
    time.sleep(5)

    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    last_comment = None
    for i in range(rep_num):
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.3)

        last_comment = driver.find_element(
            By.XPATH, "(//*[@id='content-text'])[last()]")
        last_comment.location_once_scrolled_into_view

    time.sleep(3)

    comments = driver.find_elements(By.XPATH, "//*[@id='content-text']")
    authors = driver.find_elements(By.XPATH, "//*[@id='author-text']")
    votes = driver.find_elements(By.XPATH, "//*[@id='vote-count-middle']")
    written_times = driver.find_elements(
        By.XPATH, "//*[@id='published-time-text']")

    print("==========================================")
    print(written_times)
    print("==========================================")

    data = []
    print(0)
    for author, comment, vote, written_time in zip(authors, comments, votes, written_times):
        data.append({
            'URL': url,
            'Author': author.text,
            'Comment': comment.text,
            'Votes': vote.text,
            'WrittenTime': written_time.text
        })
    print(1)
    df = pd.DataFrame(data)
    print(2)
    df.to_csv(f'./youtube_comments_{i}.csv')
    print(3)
    driver.quit()

    print("\n")
    print("="*20)
    print("done")
    print("="*20)

    return 1


df = pd.read_csv('./links.csv')
print(df)


for i, url in enumerate(df['link']):
    try:
        print("===", i, url)
        get_total_youtube_comments(url, i)
    except Exception as e:
        print("====errr ", e)
