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


def postpaid(url):
    output = None
    driver_service = Service(executable_path="chromedriver")
    driver_options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=driver_service, options=driver_options)
    browser.maximize_window()
    browser.get(url)

    html = browser.page_source
    soup = BeautifulSoup(html, "html5lib")
    plan_list = soup.find_all('div', attrs={'id': re.compile('^postpaid')})

    for plan in plan_list:
        temp = {
            'plan_name' : [plan['id']],
            'plan_quota' : [plan.find_all('div', attrs={'class':'x-plan-header-quota'})[0].text],
            'plan_price' : [plan.find_all('div', attrs={'class':'x-plan-bottom-price-text'})[0].text],
            'plan_calls' : [(str(plan.find_all('div', attrs={'class':'x-plan-bottom-usp-text'})[0]).split('>'))[1].split('<')[0].replace('\xa0', '')],
            'plan_sms' : [(str(plan.find_all('div', attrs={'class':'x-plan-bottom-usp-text'})[0]).split('>'))[4].split('<')[0].replace('\xa0', '')]
        }
        temp = pd.DataFrame.from_dict(temp)
        if output is None:
            output = temp
        else:
            output = output.append(temp)
    browser.close()
    browser.quit()
    return (output)

def postpaid_family(url):
    output = None
    driver_service = Service(executable_path="chromedriver")
    driver_options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=driver_service, options=driver_options)
    browser.maximize_window()
    browser.get(url)

    html = browser.page_source
    soup = BeautifulSoup(html, "html5lib")
    plan_list = soup.find_all('div', attrs={'class': re.compile('^x-table-plan-container x-tbc-new w-slide')})

    for plan in plan_list:
        temp = {
            'plan_name' : [plan.find_all('div', attrs={'class':'x-plan-header-name'})[0].text],
            'plan_quota' : [plan.find_all('div', attrs={'class':'x-plan-header-quota'})[0].text],
            'plan_price' : [plan.find_all('div', attrs={'class':'x-plan-bottom-price-text'})[0].text],
            'plan_calls' : [(str(plan.find_all('div', attrs={'class':'x-plan-bottom-usp-text'})[0]).split('>'))[1].split('<')[0].replace('\xa0', '')],
            'plan_sms' : [(str(plan.find_all('div', attrs={'class':'x-plan-bottom-usp-text'})[0]).split('>'))[2].split('<')[0].replace('\xa0', '')]
        }
        temp = pd.DataFrame.from_dict(temp)
        if output is None:
            output = temp
        else:
            output = output.append(temp)
    browser.close()
    browser.quit()
    return (output)


output_folder = 'C:\\Users\\AyeshaKasturiarachch\\OneDrive\\OneDrive - ADA Asia\\ADA\\Web Scraping\\Telco Devices\\Output'

url = 'https://www.digi.com.my/postpaid'
postpaid_df = postpaid(url)

url = 'https://www.digi.com.my/postpaid/family'
postpaid_family_df = postpaid_family(url)

postpaid_df = postpaid_df.append(postpaid_family_df)
postpaid_df.to_csv(output_folder+'\\DiGi_Postpaid.csv', index=False)

print('done')