# -*- coding: UTF-8 -*-
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import csv
import re
import os
import glob
import pandas as pd

def Get_Content(driver, page, post_id):
    base_url = "https://www.facebook.com/"
    try:
        driver.get(base_url + page + '/posts/' + post_id)
        sleep(randint(0,1))
        js = "return document.querySelector('._5pbx.userContent._3576').textContent;"
        content = driver.execute_script(js)
        print('Posts '+ page + '/' + post_id + ' is done.')
        return content
    except Exception as e:
        print('Posts '+ page + '/' + post_id + ' contained no text message.')
        print(e)
        return None

# get files dir
files_path = os.getcwd() + '/postid_files/'
# file_list = os.listdir(files_path)
csv_list = glob.glob("postid_files/*.csv")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome("../driver/chromedriver", options=chrome_options)

for f in csv_list:
    # read posts data from csv file
    post_df = pd.read_csv(f, encoding='utf-8-sig')
    post_header = list(post_df)
    post_list = post_df.values.tolist()
    page = re.match(r"^.*\/(.*)\_.*$", f).group(1)

    content_list = []
    error_list = []
    for post in post_list:
        post_id = str(post[0]) 
        content = Get_Content(driver, page, post_id)
        if content != None:
            content_list.append(content)
        else:
            content_list.append(content)
            error_list.append([page, post_id])
        sleep(randint(3,5))

    # save contents of each posts
    content_df = pd.DataFrame({'Content': content_list})
    df = pd.concat([post_df, content_df], axis=1)
    df.to_csv('content_files/'+ page +'_content.csv', encoding='utf-8-sig', index=False)

    # save post_id of posts without text message
    with open('error_files/error_list.txt', 'w') as err_file:
        for i in error_list:
            page = i[0]
            post_id = i[1]
            err_file.write(page + '/' + post_id + '\n')
driver.quit()