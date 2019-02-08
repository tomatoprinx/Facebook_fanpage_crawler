from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import pandas as pd
import os
import glob

def catch_screen(driver, page, post_id, path):
    base_url = "https://www.facebook.com/"
    driver.get(base_url + page + '/posts/' + post_id)
    
    # remove banner below
    js = "document.getElementById('headerArea').remove();"
    driver.execute_script(js)

    screenshot = driver.save_screenshot(path + post_id + '.png')


# get files dir
files_path = os.getcwd() + '/postid_files/'
# file_list = os.listdir(files_path)
csv_list = glob.glob("postid_files/*.csv")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--kiosk')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1440x900')
driver = webdriver.Chrome("../driver/chromedriver", options=chrome_options)

for f in csv_list:
    # read posts data from csv file
    post_df = pd.read_csv(f, encoding='utf-8-sig')
    post_list = post_df.values.tolist()
    page = re.match(r"^.*\/(.*)\_.*$", f).group(1)
    path = 'screen_shots/' + page + '/'
    if not os.path.isdir(path):
        os.mkdir(path)
    for post in post_list:
        post_id = str(post[0])
        catch_screen(driver, page, post_id, path)
        print('posts/' + post_id + ' done.')

driver.quit()