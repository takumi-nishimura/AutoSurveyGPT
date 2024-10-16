import os
import time

from selenium import webdriver

chrome_profile_dir = "chrome_profile"
os.makedirs(chrome_profile_dir, exist_ok=True)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={chrome_profile_dir}")

browser = webdriver.Chrome(options=chrome_options)
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
