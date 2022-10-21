import pandas as pd
from datetime import datetime
import time
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import glob

now = datetime.now()
date = now.date()

df_temp = pd.DataFrame(columns=['plan', 'add_on', 'description_1', 'description_2'])


# get the prepaid and family plans
def get_plans():
    plans_continer = soup.find_all('div', attrs={'class': 'x-content-wrapper'})

    for plan in plans_continer:
        get_id_desc(plan)

    # save to csv file
    df_temp.to_csv(output_folder+'\\DiGi_Add_On.csv', index=False)


def get_id_desc(obj_soup):
    # get ids container
    tabs = obj_soup.find_all('a', attrs={'class': 'w-tab-link', 'role': 'tab'})

    for tab in tabs:
        id = tab['data-w-tab']
        plan = tab.find('div').text
        # print('id :', id)
        # print('plan :', plan)

        plan_desc = obj_soup.find('div', attrs={'class': ['x-tab-pane w-tab-pane', 'w--tab-active'], 'role': 'tabpanel',
                                                'data-w-tab': id})

        addon_cards = plan_desc.find_all('div', attrs={'class': 'x-add-on-card'})
        for addon_card in addon_cards:
            # header
            header_h4 = addon_card.find('h4', attrs={'class': 'x-add-on-card-header'})
            header = header_h4.find('span').text
            # print('header :', header)

            # card desc
            cards_desc = addon_card.find_all('div', attrs={'class': 'x-add-on-card-description'})
            desc = ''
            for card_desc in cards_desc:
                desc_temp = card_desc.text
                desc = desc + ' ' + desc_temp
            # print('desc :', desc)

            # addon bold text
            cards_bold_desc = addon_card.find('div', attrs={'class': 'x-add-on-bolded-text'})
            bold_desc = ''
            if cards_bold_desc:
                bold_desc = cards_bold_desc.text
            # print('bold_desc :', bold_desc)

            # add to dataframe
            global df_temp

            df_temp = df_temp.append({
                'plan': plan,
                'add_on': header,
                'description_1': desc,
                'description_2': bold_desc
            }, ignore_index=True)


if __name__ == '__main__':
    url = 'https://www.digi.com.my/postpaid/add-ons'
    output_folder = 'C:\\Users\\AyeshaKasturiarachch\\OneDrive\\OneDrive - ADA Asia\\ADA\\Web Scraping\\Telco Devices\\Output\\add ons'

    # selenium 3 
    driver_location = 'chromedriver.exe'
    driver_options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(executable_path=driver_location, options=driver_options)

    browser.maximize_window()
    browser.get(url)

    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    table = get_plans()
    print('COMPLETED')