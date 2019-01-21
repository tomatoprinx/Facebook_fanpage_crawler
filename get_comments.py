# -*- coding: UTF-8 -*-
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
import pandas as pd
import csv
import re
import os
import glob

def Open_Comments(driver, page, post_id):
    base_url = "https://www.facebook.com/"
    driver.get(base_url + page + '/posts/' + post_id)
    sleep(randint(2,3))

    # remove banner below
    js = "document.getElementById('headerArea').remove();"
    driver.execute_script(js)

    # click to open comments
    ele = driver.find_element_by_class_name('_2u_j')
    ele.click()

    # 查看更多留言、查看更多回覆(view more comments)
    while True:
        try:
            # wait for loading cycle icon to disappear
            WebDriverWait(driver, 8).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.mls.img._55ym._55yn._55yo'))
            )
            pager = WebDriverWait(driver, 8).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'UFIPagerLink'))
            )
            pager.click()
        except StaleElementReferenceException:
            print('element not attached to the page')
        except TimeoutException:
            print('done "view more comments"')
            break

    # 查看更多(see more)
    def find(driver):
        element = driver.find_elements(By.CSS_SELECTOR, '._5v47.fss')
        if element:
            return element
        else:
            return False

    while True:
        try:
            more = WebDriverWait(driver, 5).until(find)
            for ele in more:
                ele.click()
        except TimeoutException:
            print('done "see more"')
            break

    # 點擊n則回覆(view n replies)
    def View_N_replies():
        while True:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.UFIReplySocialSentenceLinkText.UFIReplySocialSentenceVerified'))
                )
                for ele in element:
                    ele.click()
                    sleep(randint(1,3))
            except TimeoutException: 
                print('done "n replies"')
                break

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=1920,1080");
chrome_options.add_argument("--start-maximized");
driver = webdriver.Chrome("../driver/chromedriver", options=chrome_options)

# get files dir
files_path = os.getcwd() + '/postid_files/'
csv_list = glob.glob("postid_files/*.csv")

for f in csv_list:
    # read posts data from csv file
    post_df = pd.read_csv(f, encoding='utf-8-sig')
    post_list = post_df.values.tolist()
    page = re.match(r"^.*\/(.*)\_.*$", f).group(1)

    for post in post_list:
        print('***************post***************')
        post_id = str(post[0])
        Open_Comments(driver, page, post_id)

        # 獲取留言內容(get comment)
        comment = driver.find_elements_by_css_selector('.UFICommentBody')
        comment_list = []
        for i in comment:
            comment_list.append(i.text)
        # print(comment_list)

        path = 'comment_files/' + page + '/'
        if not os.path.isdir(path):
            os.mkdir(path)

        with open(path + post_id + '_comments.csv', 'w', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            for row in comment_list:
                writer.writerow([row])
driver.quit()