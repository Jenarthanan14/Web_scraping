# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
import os
import csv
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
from datetime import datetime
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import glob

now = datetime.now()
date = now.date()

in_path = 'C:\\Users\\AyeshaKasturiarachch\\OneDrive\\OneDrive - ADA Asia\\ADA\\Web Scraping\\Telco Devices\\Output'
out_path = 'C:\\Users\\AyeshaKasturiarachch\\OneDrive\\OneDrive - ADA Asia\\ADA\\Web Scraping\\Telco Devices\\Final Output'

def scrape_device_data(device, url):
    try:
        output = None
        delay = 30
        driver_service = Service(executable_path="chromedriver")
        driver_options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(service=driver_service, options=driver_options)
        browser.maximize_window()
        browser.implicitly_wait(delay)
        browser.get(url)
        browser.implicitly_wait(30)

        # click 'Buy now'
        # check if there's OOS
        buy_now_button = browser.find_elements(By.XPATH, '//*[@id="selectButton"]')
        try:
            browser.execute_script("arguments[0].click();", buy_now_button[0])
        except:
            print('{} not available'. format(device))
            return pd.DataFrame.from_dict({
                'carrier': ['DiGi'],
                'currency': ['RM'],
                'device_name': [device],
                'device_brand': [''],
                'device_colour': [''],
                'device_storage': [''],
                'device_availability': ['Device not available'],
                'rrp': [''],
                'plan': [''],
                'pay_now_total': [''],
                'pay_now_device': [''],
                'pay_now_device_advance_payment': [''],
                'pay_now_device_advance_payment_remarks': [''],
                'pay_now_plan_advance_payment': [''],
                'pay_now_plan_advance_payment_remarks': [''],
                'monthly_charge_total': [''],
                'monthly_charge_device_installment': [''],
                'monthly_charge_plan_rate': [''],
                'url':[url]
            })

        # colour list
        html = browser.page_source
        soup = BeautifulSoup(html, "html5lib")
        colour_list = [x.get_text() for x in
                        soup.find_all('div', attrs={'id': re.compile('^edit-color')})[0].find_all('span')]

        # colour_list = browser.find_elements(By.XPATH, '//div[@id="edit-color"]//child::label')

        for colour in colour_list:
            # browser.execute_script("arguments[0].click();", colour)

            colourFlag = True
            while colourFlag:
                try:
                    contracts = browser.find_elements(By.XPATH,
                                                      "//*[starts-with(@id,'edit-color')]//child::span[contains(text(),'" + colour + "')]")
                    browser.execute_script("arguments[0].click();", contracts[0])
                    colourFlag = False
                    print("try colour")
                except:
                    print("except colour")

            time.sleep(15)

            html = browser.page_source
            soup = BeautifulSoup(html, "html5lib")
            storage_list = [x.get_text() for x in
                            soup.find_all('div', attrs={'id': re.compile('^edit-storage')})[0].find_all('span')]

            # storage_xpath = "//*[@id='edit-storage']//child::span"
            # storage_list = browser.find_elements(By.XPATH, storage_xpath)

            for storage in storage_list:

                storageFlag = True
                while storageFlag:
                    try:
                        contracts = browser.find_elements(By.XPATH,
                                                          "//*[starts-with(@id,'edit-storage')]//child::span[contains(text(),'" + storage + "')]")
                        browser.execute_script("arguments[0].click();", contracts[0])
                        storageFlag = False
                        print("try storage")
                    except:
                        print("except storage")

                # browser.execute_script("arguments[0].click();", storage)

                time.sleep(10)

                # click 'New Line'
                new_line_button = browser.find_elements(By.XPATH, '//*[@id="edit-order-type"]/div[1]/label')
                browser.execute_script("arguments[0].click();", new_line_button[0])

                time.sleep(10)

                # select plans
                select_plans_xpath = "//div[@class='plan-configuration-panel']//child::div[starts-with(@id, 'edit-plans')]//child::img"
                select_plans = browser.find_elements(By.XPATH, select_plans_xpath)

                for select_plan in select_plans:
                    browser.execute_script("arguments[0].click();", select_plan)

                    time.sleep(5)

                    # scrape data
                    rrp = browser.find_elements(By.XPATH,
                        '/html/body/div[1]/div/div[2]/div/div[2]/section/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/div/div/div[3]/div/div/span/del')[
                        0].text
                    try:
                        device_brand = browser.find_elements(By.XPATH,
                            '/html/body/div[1]/div/div[2]/div/div[2]/section/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/div/div/ul/li')[
                            0].text
                    except:
                        device_brand = 'not mentioned'

                    device_name = browser.find_elements(By.XPATH, '//*[@id="pdp-price-summary-name"]')[0].text
                    device_colour = browser.find_elements(By.XPATH, '//*[@id="pdp-price-summary-color"]')[0].text.strip(
                        ',')
                    device_storage = browser.find_elements(By.XPATH, '//*[@id="pdp-price-summary-storage"]')[0].text
                    device_availability = browser.find_elements(By.XPATH,'//*[@id="pdp-low-stock-wrapper"]/div')[0].text

                    plan = browser.find_elements(By.XPATH,
                        '/html/body/div[1]/div/div[2]/div/div[2]/section/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/div/div/div[3]/div/div')[
                        0].text.split('\n')[-1]
                    pay_now_total = browser.find_elements(By.XPATH, '//*[@id="pdp-price-summary-total-due-today"]')[
                        0].text
                    pay_now_device = browser.find_elements(By.XPATH, '//*[@id="pdp-price-summary-price"]')[0].text
                    pay_now_device_advance_payment = \
                    browser.find_elements(By.XPATH, '//*[@id="pdp-device-upfront-payment"]')[0].text
                    pay_now_device_advance_payment_remarks = \
                    browser.find_elements(By.XPATH, '//*[@id="contract_rebate_months_text"]')[0].text
                    pay_now_plan_advance_payment = \
                    browser.find_elements(By.XPATH, '//*[@id="pdp-plan-advance-payment"]')[0].text
                    pay_now_plan_advance_payment_remarks = \
                    browser.find_elements(By.XPATH, '//*[@id="pdp-plan-advance-payment-wrapper"]/div[1]/span')[0].text
                    monthly_charge_total = \
                    browser.find_elements(By.XPATH, '//*[@id="pdp-price-summary-total-due-today-btl"]')[0].text
                    monthly_charge_device_installment = \
                    browser.find_elements(By.XPATH, '//*[@id="device_installation_btl_value"]')[0].text
                    monthly_charge_plan_rate = browser.find_elements(By.XPATH, '//*[@id="plan_rate_btl_value"]')[0].text

                    temp = {
                        'carrier': ['DiGi'],
                        'currency': ['RM'],
                        'device_name': [device_name],
                        'device_brand': [device_brand],
                        'device_colour': [device_colour],
                        'device_storage': [device_storage],
                        'device_availability': [device_availability],
                        'rrp': [rrp],
                        'plan': [plan],
                        'pay_now_total': [pay_now_total],
                        'pay_now_device': [pay_now_device],
                        'pay_now_device_advance_payment': [pay_now_device_advance_payment],
                        'pay_now_device_advance_payment_remarks': [pay_now_device_advance_payment_remarks],
                        'pay_now_plan_advance_payment': [pay_now_plan_advance_payment],
                        'pay_now_plan_advance_payment_remarks': [pay_now_plan_advance_payment_remarks],
                        'monthly_charge_total': [monthly_charge_total],
                        'monthly_charge_device_installment': [monthly_charge_device_installment],
                        'monthly_charge_plan_rate': [monthly_charge_plan_rate],
                        'url':[url]
                    }

                    print('\n {}'.format(temp))

                    temp = pd.DataFrame.from_dict(temp)
                    if output is None:
                        output = temp
                    else:
                        output = output.append(temp)

        browser.close()
        browser.quit()
        # output  # remove
        return (output)
    except:
        print('{} ended with error'.format(device))


l1_url_list = ['https://www.digi.com.my/devices/android','https://www.digi.com.my/devices/iphones']


for l1_url in l1_url_list:
    browser = webdriver.Chrome(executable_path='chromedriver.exe')
    browser.get(l1_url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html5lib")
    l2_url_list = soup.find_all('a', attrs={'class': 'x-plan-table-row w-inline-block'})

    for i in range(0, len(l2_url_list)):
        url = l2_url_list[i]['href']
        device = l2_url_list[i].text
        csv_files = glob.glob(os.path.join(in_path, "*.csv"))
        csv_files = [sub.replace(in_path+'\\', '') for sub in csv_files]
        csv_files = [sub.replace('_info.csv', '') for sub in csv_files]

        # save details for each device as one csv, check whether the same device is repeated
        if device.split(':')[0] not in csv_files:
            print('{} started'.format(device))
            print(url)
            df = scrape_device_data(device, url)

            if df is not None:
                df.to_csv('{}\\{}_info.csv'.format(in_path, device.split(':')[0]), index=False)
                print('{} completed successfully'.format(device))
            else:
                print('{} returned empty dataframe'.format(device))
        else:
            print('{} is already scraped'.format(device))

# merge all csvs
csv_files = glob.glob(os.path.join(in_path, "*.csv"))
print(len(csv_files))

final_df = None

for f in csv_files:
    # read the csv file
    df = pd.read_csv(f)
    if final_df is None:
        final_df = df
    else:
        final_df = final_df.append(df)

final_df = final_df.drop_duplicates()
final_df = final_df.fillna(value={'device_availability': 'Device not available'})