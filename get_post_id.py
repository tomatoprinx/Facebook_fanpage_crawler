# -*- coding: UTF-8 -*-
import time
import csv
import re
import json
import pandas as pd
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class FacebookPostIdScraper():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome("../driver/chromedriver", options=chrome_options)

    def get_last_post_time(self, page):
        # get the timestamp of the last rendered post
        test = self.driver.find_elements_by_css_selector('div[style="padding-top:8px"]>div>div>article')
        last_post = json.loads(test[-1].get_attribute('data-ft'))
        page_id = last_post['page_id']
        last_post_time = last_post['page_insights'][page_id]['post_context']['publish_time']
        # print('[Running ' + page + ']found ', len(test), ' posts.')
        return last_post_time

    def get_post_id(self, page, begin_catch_time, end_catch_time):
        url = "https://m.facebook.com/pg/" + page + "/posts/"
        self.driver.get(url)

        last_post_time = time.time() # current timestamp
        while last_post_time > begin_catch_time:
            js = "window.scrollTo(0, document.body.scrollHeight);"
            self.driver.execute_script(js)
            last_post_time = self.get_last_post_time(page)

        raw_feed = [i.get_attribute('data-ft') for i in self.driver.find_elements_by_css_selector('._56be._4hkg._5rgr._3drq.async_like')]
        feed_list = []
        time_list = []
        for feed in raw_feed:
            # convert string into json
            feed = json.loads(feed)
            page_id = feed['page_id']
            feed_list.append(feed['top_level_post_id'])
            time_list.append(feed['page_insights'][page_id]['post_context']['publish_time'])
        
        feed_df = pd.DataFrame({'Post_Id': feed_list, 'Publish_Time': time_list})
        feed_df['Page'] = page
        feed_df = feed_df.loc[(feed_df['Publish_Time'] >= begin_catch_time) & (feed_df['Publish_Time'] <= end_catch_time)]
        print('Done! Collected ', len(feed_df), ' posts from ' + page)

        return feed_df

if __name__ =='__main__':
    
    postid_scraper = FacebookPostIdScraper()
    
    # set a date for scraper to catch post published between its timestamp
    begin_date = "2018-12-31"
    end_date = "2019-01-25"
    begin_catch_time = int(time.mktime(time.strptime(begin_date, "%Y-%m-%d")))
    end_catch_time = int(time.mktime(time.strptime(end_date, "%Y-%m-%d")))

    with open('page_list/fanpages.txt') as f:
        page_list = f.readlines()
    page_list = [i.strip() for i in page_list]
    for page in page_list:
        feed_df = postid_scraper.get_post_id(page, begin_catch_time, end_catch_time)
        feed_df.to_csv('postid_files/' + page + '_postid2.csv', encoding='utf-8-sig', index=False)