from selenium.webdriver.chrome.service import Service
import re
import os
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import glob

now = datetime.now()
date = now.date()


def prepaid_1(url):
    output = None
    driver_service = Service(executable_path="chromedriver")
    driver_options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=driver_service, options=driver_options)
    browser.maximize_window()
    browser.get(url)

    html = browser.page_source
    soup = BeautifulSoup(html, "html5lib")
    plan_list = soup.find_all('div', attrs={'class': re.compile('^x-plan-container')})

    for plan in plan_list:
        temp = {
            'plan_name' : [plan.find_all('div', attrs={'class':'x-plan-header-name'})[0].text.replace('\xa0', '')],
            'plan_quota' : [plan.find_all('div', attrs={'class':'x-plan-header-quota'})[0].text.replace('\xa0', '')],
            'plan_price' : [plan.find_all('div', attrs={'class':'x-plan-bottom-price-text'})[0].text.replace('\xa0', '')],
            'plan_description_1' : [plan.find_all('div', attrs={'class':'x-auto-renewal-text'})[0].text.replace('\xa0', '')],
            'plan_description_2' : [plan.find_all('div', attrs={'class':'x-auto-renewal-text'})[1].text.replace('\xa0', '')]
        }
        temp = pd.DataFrame.from_dict(temp)
        if output is None:
            output = temp
        else:
            output = output.append(temp)
    browser.close()
    browser.quit()
    return (output)

def prepaid_2(url):
    output = None
    driver_service = Service(executable_path="chromedriver")
    driver_options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=driver_service, options=driver_options)
    browser.maximize_window()
    browser.get(url)

    html = browser.page_source
    soup = BeautifulSoup(html, "html5lib")
    table_list = soup.find_all('div', attrs={'class': 'x-plan-table-block'})

    for table in table_list:
        sidebar_list = table.find_all('div', attrs={'class': 'x-plan-table-sidebar'})[0].find_all('div', attrs={'class': 'x-emp-text'})
        column_list = [x.text.replace('\xa0', '') for x in sidebar_list]
        sidebar_header = table.find_all('div', attrs={'class': 'x-plan-table-sidebar'})[0].find('h3').text.replace('\xa0', '')

        plan_list = table.find_all('div', attrs={'class': 'x-plan-table-col'})

        for plan in plan_list:
            temp = {
            'plan_type' : [sidebar_header],
            'plan_name': [plan.find('div', attrs={'class': 'x-emp-text for-title'}).text.replace('\xa0', '')],
            'plan_price' : [plan.find_all('div', attrs={'class': 'x-emp-text'})[1].text.replace('\xa0', '')]
            }

            for i in range(len(column_list)):
                value = plan.find_all('div', attrs={'class': re.compile('^x-plan-table-row for-center')})[i]
                if bool(value.find_all('div', attrs={'class': 'x-icon for-plan-table is-green'})):
                    temp[column_list[i]] = 'yes'
                elif bool(value.find_all('div', attrs={'class': 'x-icon for-plan-table is-red'})):
                    temp[column_list[i]] = 'no'
                else:
                    temp[column_list[i]] = value.text.replace('\xa0', '')

            temp = pd.DataFrame.from_dict(temp)
            if output is None:
                output = temp
            else:
                output = output.append(temp)
    browser.close()
    browser.quit()
    return (output)


output_folder = 'C:\\Users\\AyeshaKasturiarachch\\OneDrive\\OneDrive - ADA Asia\\ADA\\Web Scraping\\Telco Devices\\Output'

url = 'https://www.digi.com.my/prepaid'
prepaid_1_df = prepaid_1(url)
prepaid_2_df = prepaid_2(url)

prepaid_df = prepaid_1_df.append(prepaid_2_df)
prepaid_df.to_csv(output_folder + '\\DiGi_Postpaid.csv', index=False)

print('done')