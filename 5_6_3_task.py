# Задача на степике https://stepik.org/lesson/1108387/step/6?unit=1119656

import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By


base_url = '...'

with webdriver.Chrome() as webdriver:
    webdriver.get(base_url + 'index.html')
    link_tags = webdriver.find_elements(By.TAG_NAME, 'a')
    list_url = [link_tag.get_attribute('href') for link_tag in webdriver.find_elements(By.TAG_NAME, 'a')]

    list_expiry = {}
    for url in list_url:
        webdriver.get(url)
        cookies = webdriver.get_cookies()
        for cookie in cookies:
            list_expiry[url] = cookie['expiry']

    ssd = sorted(list_expiry, key=list_expiry.__getitem__)
    k = ssd[-1]
    webdriver.get(k)
    print(webdriver.find_element(By.ID, 'result').text)  
