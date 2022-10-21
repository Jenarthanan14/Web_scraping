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
from selenium.webdriver.support import expected_conditions as EC
now = datetime.now()
date = now.date()
import re
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager




#https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-z-flip-3-5g
#https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-12-pro-max


now = datetime.now()
extraxtion_date = now.date()
date = extraxtion_date.strftime("%Y%m%d")
path = 'Maxis/'+  date + '/'              
if not os.path.exists(path):
    os.makedirs(path)

urls = ['https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-13-pro-max','https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-13-pro',
        'https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-13','https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-s21-fe-5g',
        'https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-z-fold3-5g','https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-z-flip-3-5g',
        'https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-s21-ultra-5g','https://store.maxis.com.my/productdetails/category/mobiles/oppo/find-x3-pro',
        'https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-12-pro-max','https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-12-pro',
        'https://store.maxis.com.my/productdetails/category/mobiles/asus/rog-phone-5s','https://store.maxis.com.my/productdetails/category/mobiles/xiaomi/black-shark-4',
        'https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-12','https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-13-mini',
        'https://store.maxis.com.my/productdetails/category/mobiles/asus/rog-phone-5','https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-12-mini',
        'https://store.maxis.com.my/productdetails/category/mobiles/oppo/reno6-pro-5g','https://store.maxis.com.my/productdetails/category/mobiles/realme/gt-master-edition',
        'https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-s20-fe-5g','https://store.maxis.com.my/productdetails/category/mobiles/vivo/y20-2021',
        'https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-a12','https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-xr',
        'https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-a32-5g','https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-a52',
        'https://store.maxis.com.my/productdetails/category/mobiles/oppo/a54','https://store.maxis.com.my/productdetails/category/mobiles/vivo/v21e',
        'https://store.maxis.com.my/productdetails/category/mobiles/vivo/v21','https://store.maxis.com.my/productdetails/category/mobiles/realme/8-pro',
        'https://store.maxis.com.my/productdetails/category/mobiles/vivo/v21-5g','https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-a22-5g',
        'https://store.maxis.com.my/productdetails/category/mobiles/huawei/nova-8i','https://store.maxis.com.my/productdetails/category/mobiles/oppo/reno6-z-5g',
        'https://store.maxis.com.my/productdetails/category/mobiles/vivo/y31','https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-s21-5g',
        'https://store.maxis.com.my/productdetails/category/mobiles/xiaomi/redmi-10','https://store.maxis.com.my/productdetails/category/mobiles/oppo/reno6-5g',
        'https://store.maxis.com.my/productdetails/category/mobiles/realme/c25y','https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-a03s',
        'https://store.maxis.com.my/productdetails/category/mobiles/vivo/x70','https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-a52s-5g',
        'https://store.maxis.com.my/productdetails/category/mobiles/honor/50','https://store.maxis.com.my/productdetails/category/mobiles/huawei/nova-9',
        'https://store.maxis.com.my/productdetails/category/mobiles/samsung/galaxy-m12','https://store.maxis.com.my/productdetails/category/mobiles/oppo/a95',
        'https://store.maxis.com.my/productdetails/category/mobiles/vivo/y76-5g','https://store.maxis.com.my/productdetails/category/mobiles/honor/50-lite',
        'https://store.maxis.com.my/productdetails/category/mobiles/vivo/y15a','https://store.maxis.com.my/productdetails/category/mobiles/apple/iphone-11',
        'https://store.maxis.com.my/productdetails/category/mobiles/vivo/v23e','https://store.maxis.com.my/productdetails/category/mobiles/vivo/x60',
        'https://store.maxis.com.my/productdetails/category/mobiles/vivo/v21e-biggest-sale'
    ]

for url in urls[3:]:
    options = webdriver.ChromeOptions()
##    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument("--incognito")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    browser.get(url)
    html_source_code = browser.execute_script("return document.innerHTML;")
    browser.set_page_load_timeout(10)

    html = browser.page_source
    soup = BeautifulSoup(html, "html5lib")
    browser.implicitly_wait(10)
    contracts = list(set(soup.find_all('div', attrs = {'id':'devicePlans'})[0].find_all('div', attrs = {'class':'upper-content'})[1].find_all('div', attrs = {'class':'slick-list'})[0].find_all('button', attrs = {'type':'button'})))

    df_final = pd.DataFrame(columns=['Divice_Name', 'Divice_Brand','Extraxtion_Date','Contract_Option', 'Colour', 'Storage_Size', 'Package_Name','Monthly_Device_Instalment',
                    'Plan_Monthly_Charges','Total_Monthly_Payment','Device_Price', 'Upfront_Payment', 'Availability'])
    
    for contract in contracts:
        contract_id = contract['id']
        button_contract = browser.find_element(By.XPATH,"//button[@id='"+contract_id+"']")
        browser.execute_script("arguments[0].click();", button_contract)
        browser.implicitly_wait(10)
        contracts = browser.find_elements(By.XPATH,"//span[contains(text(),'SELECT')]")
        print(len(contracts))
        for contract in contracts:
            browser.execute_script("arguments[0].click();", contract)
            browser.implicitly_wait(10)
            storages = browser.find_elements(By.XPATH,"//div[@id='storage-section']//child::p")
            for storage in range(1,len(storages)): 
                browser.execute_script("arguments[0].click();", storages[storage])
                browser.implicitly_wait(10)
                colours = browser.find_elements(By.XPATH,"//div[@id='colors-section']//child::span")
                for colour in colours: 
                    browser.execute_script("arguments[0].click();", colour)
                    browser.implicitly_wait(10)
                    html_source_code = browser.execute_script("return document.innerHTML;")
                    browser.set_page_load_timeout(10)

                    html = browser.page_source
                    soup = BeautifulSoup(html, "html5lib")
                    browser.implicitly_wait(10)
                    
                    device_name = soup.find_all('div', attrs = {'id':'pdp-cart-section'})[0].find_all('div', attrs = {'class':'col-4 cart-details'})[0].find_all('div', attrs = {'class':'d-flex text-gunmetal mt-1'})[0].find_all('span')[0].text
                    device_brand = soup.find_all('div', attrs = {'id':'brand-section'})[0].find_all('p')[-1].text
                    colour = ' '.join(soup.find_all('div', attrs = {'id':'pdp-cart-section'})[0].find_all('div', attrs = {'class':'col-4 cart-details'})[0].find_all('div', attrs = {'class':'d-flex text-gunmetal mt-1'})[0].find_all('span')[1].text.split('/')[0].strip().split()[1:])
                    storage = soup.find_all('div', attrs = {'id':'pdp-cart-section'})[0].find_all('div', attrs = {'class':'col-4 cart-details'})[0].find_all('div', attrs = {'class':'d-flex text-gunmetal mt-1'})[0].find_all('span')[1].text.split('/')[1].strip()
                    contract_option = soup.find_all('div', attrs = {'id':'pdp-cart-section'})[0].find_all('div', attrs = {'class':'col-4 cart-details'})[0].find_all('div', attrs = {'class':'text-left col-6'})[0].text.split('/')[1].strip()
                    package_name = soup.find_all('div', attrs = {'id':'pdp-cart-section'})[0].find_all('div', attrs = {'class':'col-4 cart-details'})[0].find_all('div', attrs = {'class':'text-left col-6'})[1].text.strip()
                    monthly_device_Instalment = soup.find_all('div', attrs = {'id':'pdp-cart-section'})[0].find_all('div', attrs = {'class':'col-4 cart-details'})[0].find_all('div', attrs = {'class':'text-blue-green text-right col-6'})[0].text.replace(",", "")
                    plan_monthly_charges = soup.find_all('div', attrs = {'id':'pdp-cart-section'})[0].find_all('div', attrs = {'class':'col-4 cart-details'})[0].find_all('div', attrs = {'class':'text-blue-green text-right col-6'})[1].text.replace(",", "")
                    total_monthly_payment = soup.find_all('div', attrs = {'id':'pdp-cart-section'})[0].find_all('div', attrs = {'class':'col-3 col-xl-2 text-gunmetal pl-4'})[0].find_all('span')[0].text.replace(",", "")
                    upfront_payment = soup.find_all('div', attrs = {'id':'pdp-cart-section'})[0].find_all('div', attrs = {'class':'col-2 px-0'})[0].find_all('span')[0].text.replace("*", "").replace(",", "")
                    availability = soup.find_all('div', attrs = {'id':'pdp-cart-section'})[0].find_all('button', attrs = {'id':'dBtnAddToCart'})[0].text


                    df_final = df_final.append({'Divice_Name': device_name, 'Divice_Brand':device_brand,'Extraxtion_Date': extraxtion_date,'Contract_Option': contract_option, 'Colour':colour, 'Storage_Size': storage, 'Package_Name':package_name,'Monthly_Device_Instalment': monthly_device_Instalment,
                        'Plan_Monthly_Charges': plan_monthly_charges,'Total_Monthly_Payment': total_monthly_payment,'Device_Price': None, 'Upfront_Payment': upfront_payment, 'Availability': availability }, ignore_index=True)


    df_final.to_csv(path+date+'_'+device_name+'_devices.csv', index=False)
    print('Successfully Maxis '+device_name+' Details Collected!')
    browser.quit()

