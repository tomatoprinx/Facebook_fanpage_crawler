# -*- coding: UTF-8 -*-
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import csv
import re
import pandas as pd

maxpost = 100
page = "name of fan page"
url = "https://www.facebook.com/pg/" + page + "/posts/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome("../driver/chromedriver", options=chrome_options)
driver.get(url)

# retrieve page id
page_id = re.match(r"^.*pg\/(.*)\/posts.*$", url).group(1)
    
# scroll the page to bottom to scraping content from lazy-loading page
# get feed_subtitle id
try:
    while True:
        js = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(js)
        sleep(2)

        feed_list = [i.get_attribute('value') for i in driver.find_elements_by_name('ft_ent_identifier')]
        if (len(feed_list) >= maxpost):
            print('Done! Collected ', len(feed_list), ' posts from ', page_id)
            break
finally:
    driver.quit()
    combine_df = pd.DataFrame({'Post_Id':feed_list})
    combine_df['Page_Id'] = page_id
    combine_df.to_csv('postid_files/' + page_id + '_postid.csv', encoding='utf-8-sig', index=False)