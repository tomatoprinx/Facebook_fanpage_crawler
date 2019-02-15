# -*- coding: UTF-8 -*-
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import os
import glob
import pandas as pd

def Get_Engagements(driver, page, post_id):
    base_url = "https://www.facebook.com/"
    driver.get(base_url + page + '/posts/' + post_id)
    try:
        ele = driver.find_element_by_class_name('_37uu')
        engagements = [i.text for i in driver.find_elements_by_css_selector('._524d>a>span')]
        print('Posts ' + page + '/' + post_id + ' completed.')
        return engagements
    except Exception as e:
        print(e)
        print('Posts ' + page + '/' + post_id + ' no engagement!')
        return None

# get files dir
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

    engagements_list = []
    for post in post_list:
        post_id = str(post[0]) 
        engagements = Get_Engagements(driver, page, post_id)
        engagements_list.append(engagements)

    egg_list = []
    for engagement in engagements_list:
        egg_dict = {'Comment':0, 'Share':0}
        for i in engagement:
            if "留言" in i:
                comnt_num = re.sub(r"\D", '', i)
                egg_dict['Comment'] = comnt_num
            elif "分享" in i:
                share_num = re.sub(r"\D", '', i)
                egg_dict['Share'] = share_num
        egg_list.append(egg_dict)

    # save engagements of each posts
    engagements_df = pd.DataFrame(egg_list)
    df = pd.concat([post_df, engagements_df], axis=1)
    df.to_csv('engagements_files/'+ page +'_engagements.csv', encoding='utf-8-sig', index=False)

driver.quit()