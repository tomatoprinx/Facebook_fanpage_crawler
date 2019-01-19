# -*- coding: UTF-8 -*-
from time import sleep
from random import randint
from selenium import webdriver
import pickle
import os
import re
import pandas as pd

driver = webdriver.Firefox(executable_path = "../driver/geckodriver")
driver.get("https://m.facebook.com/")
account = "your email account"
pwd = "your password"

# type in account and pwd
driver.find_element_by_id("m_login_email").send_keys(account)
driver.find_element_by_css_selector(".bl.bm.bo.bp").send_keys(pwd)
driver.find_element_by_css_selector(".n.t.o.bz.br.ca").click()
sleep(3)

def Get_Reaction(driver, page, post_id):

    base_url = "https://m.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier="
    driver.get(base_url + post_id)
    sleep(randint(1,2))
    reaction = [i.get_attribute('href') for i in driver.find_elements_by_class_name('ba')]
    # print(reaction)
    reaction_types = ['Total', '1', '2', '3', '4', '7', '8']
    react_dict = dict((el, 0) for el in reaction_types)
    for r in reaction:
        r_count = re.search(r"^.*count\=(.*)\&.*$", r).group(1)
        if re.search(r"^.*type\=(.*)\&total.*$", r) is not None:
            r_type = re.search(r"^.*type\=(.*)\&total.*$", r).group(1)
            react_dict[r_type] = r_count
        else:
            react_dict['Total'] = r_count
    print('posts ' + page + '/' + post_id + ' is done!')
    return react_dict

# get files dir
files_path = os.getcwd() + '/postid_files/'
file_list = os.listdir(files_path)

for f in file_list:
    # read posts data from csv file
    post_df = pd.read_csv('postid_files/' + f, encoding='utf-8-sig')
    post_header = list(post_df)
    post_list = post_df.values.tolist()
    page = f.split('_')[0]

    reaction_list = []
    for post in post_list:
        print('***************post***************')
        post_id = str(post[0])
        react_dict = Get_Reaction(driver, page, post_id)
        reaction_list.append(react_dict)
        print(react_dict)
        sleep(randint(1,3))

    # change lists of reaction dict into dataframe and rename column name.
    new_header = ['Like', 'Love', 'Wow', 'Haha', 'Sad', 'Angry', 'Total']
    df = pd.DataFrame(reaction_list)
    df.columns = new_header
    df['Post_Id'] = post_df['Post_Id']
    cols = ['Post_Id'] + new_header
    df = df[cols]
    
    df.to_csv('reaction_files/' + page +'_reaction.csv', encoding='utf-8-sig', index=False)
driver.quit()