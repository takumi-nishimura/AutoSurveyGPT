import json
import time

import openai
from selenium import webdriver
from selenium.webdriver.common.by import By

import config
import gpt_config
import prompt
from gpt_config import get_driver_path

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"--user-data-dir={config.chrome_user_data_dir}")

service = webdriver.ChromeService(executable_path=get_driver_path())

browser = webdriver.Chrome(service=service, options=options)
browser.implicitly_wait(5)

url = "https://www.sciencedirect.com/science/article/pii/S2666651023000141"

browser.get(url)
html = browser.page_source
txt = browser.find_element(By.XPATH, "/html/body").text

openai.api_key = config.openai_api_key
openai.api_base = config.openai_api_base

res = openai.ChatCompletion.create(
    model=gpt_config.html_parse_model,
    messages=prompt.html_parsing_prompt(txt),
)
ans = res["choices"][0]["message"]["content"]
if ans.startswith("```json"):
    ans = ans[ans.find("{") : ans.rfind("}") + 1]
jans = json.loads(ans, strict=False)
print(jans)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
