import os
import string
import pandas as pd
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# return date now
def get_date_now():
    now = datetime.now()
    date_now = now.date().strftime("%Y%m%d")

    return date_now

def save_as_csv(df: pd.DataFrame, loc_to_save: string):
    if loc_to_save.endswith('.csv'):
        df.to_csv(loc_to_save, mode='a', index=False, header=not os.path.exists(loc_to_save))

# scroll down
def scroll_down(driver):
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False

    while (match == False):
        lastCount = lenOfPage
        time.sleep(3)

        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

# initalize selenium driver
def init_driver():
    delay = 10

    # WINDOWS
    driver_location = 'C:/Users/JenarthananRajenthir/OneDrive - ADA Asia/Documents/Final_telco/Code/chromedriver.exe'

    driver_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=driver_location, options=driver_options)
    driver.maximize_window()
    driver.implicitly_wait(delay)

    return driver

# wait until a page elements loads
def wait_until_pg_load_completes(driver, xpath: str):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
    except Exception as ex:
        print('An error occured at wait_until_pg_load_completes(): ', ex.__class__)
        driver.quit()

# click view more
def click_view_more_if_exist(driver):
    btn_exist = True
    view_more_xpath = "//button[contains(text(),'View More')]"

    while (btn_exist == True):
        try:
            view_more_btn = driver.find_element(By.XPATH, view_more_xpath)
            ActionChains(driver).move_to_element(view_more_btn).pause(1).click(view_more_btn).perform()
            time.sleep(3)
        except NoSuchElementException as ex:
            btn_exist = False

# get device and plan list
def get_all_device_and_plan(url: str):
    driver = init_driver()
    driver.get(url)

    device_and_plan_xpath = "//div[starts-with(@class, 'umSwitchBox')]//a[starts-with(@class, 'umSwitchItem')]"
    tabs = driver.find_elements(By.XPATH, device_and_plan_xpath)

    base_url = "https://shop.u.com.my/um"
    
    device_plan_list_xpath = "//div[starts-with(@class, 'offerListContainer')]//div[starts-with(@class, 'umOfferItemBox')]"\
                            "//div[starts-with(@class, 'innerBox')]//div[starts-with(@class, 'offerFooter')]"\
                            "//div[starts-with(@class, 'um-btn-squarish')]"
  
    device_buy_lst = []
    plan_buy_lst = []

    # 1st tab Devices
    # 2nd tab Plans
    for idx, tab in enumerate(tabs):
        ActionChains(driver).move_to_element(tab).pause(1).click(tab).perform()

        # expand the device or plan list
        click_view_more_if_exist(driver)

        if idx == 0:
            print('== GETTING DEVICE LIST')

            # 1st tab Devices            
            device_lists = driver.find_elements(By.XPATH, device_plan_list_xpath)
            for device in device_lists:
                device_buy_lst.append(
                    {
                        'buy_now': base_url + device.get_attribute("to")
                    }
                )
        elif idx == 1:
            print('== GETTING PLAN LIST')

            # 2nd tab Plans
            plan_lists = driver.find_elements(By.XPATH, device_plan_list_xpath)
            for plan in plan_lists:
                plan_buy_lst.append(
                    {
                        'buy_now': base_url + plan.get_attribute("to")
                    }
                )
        else:
            print('A problem occured while selecting the tab - get_all_device_and_plan()')
    
    driver.quit()
    
    return device_buy_lst, plan_buy_lst
