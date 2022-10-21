from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import pandas as pd
import time
import json

import common

# plan_orchestrator() - information scraper flow
def plan_orchestrator(plans):
    for idx, plan in enumerate(plans):
        url = plan['buy_now']

        # init driver
        driver = common.init_driver()
        driver.get(url)

        # wait until page loading completed
        master_device_info_block_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]"
        common.wait_until_pg_load_completes(
            driver, master_device_info_block_xpath)

        # scroll down
        # common.scroll_down(driver)

        plan_progress = f'{idx+1}/{len(plans)}'
        fetch_and_store_plan_details(driver, url, plan_progress)
        driver.quit()

# get payment break down
def get_payment_breakdown(driver):
    payment_breakdown_xpath = "//div[@class='cart-details left-panel']//div[@class='ant-spin-container']"\
                            "//div[starts-with(@class, 'field-info')]"
    payments_breakdown = driver.find_elements(
        By.XPATH, payment_breakdown_xpath)

    _breakdown = {}
    if len(payments_breakdown) > 0:
        for payment_breakdown in payments_breakdown:
            breakdown_xpath = "//div[@class='cart-details left-panel']//div[@class='ant-spin-container']//div[starts-with(@class, 'field-info')]//span"
            breakdown = payment_breakdown.find_elements(
                By.XPATH, breakdown_xpath)

            for idx in range(0, len(breakdown), 2):
                _breakdown[breakdown[idx].text] = breakdown[idx + 1].text

            _payment_breakdown = json.dumps(_breakdown)

            return _payment_breakdown
    elif len(payments_breakdown) == 0:
        return 'No payment breakdown found'
    else:
        return 'An error occured while extracting the payment breakdown'

# get the total amount due
def get_total_due_amount(driver):
    total_due_amount_xpath = "//div[starts-with(@class, 'cart-button right-panel')]//div[@class='font-bold']//span[starts-with(@class, 'h4')]"
    total_due_amount = driver.find_element(By.XPATH, total_due_amount_xpath)
    _total_due_amount = total_due_amount.text

    return _total_due_amount

# save dataframe as csv
def save_plan_dataframe_to_csv(df: pd.DataFrame):
    # declare date
    date = common.get_date_now()

    # save the dataframe as csv
    location = './data/' + date + '_umobile_plans.csv'
    common.save_as_csv(df, location)

# get plan info blocks
# arg: selenium driver.webdriver
# return: plan details
def fetch_and_store_plan_details(driver, url: str, progress: str):
    try:
        # index
        print(progress, ' >>>')

        # device url
        _url = url
        print('Plan URL: ', _url)

        master_div_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]"
        master_div = driver.find_element(By.XPATH, master_div_xpath)

        # plan name
        name_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]//h1[starts-with(@class,'offerName')]"
        _name = master_div.find_element(By.XPATH, name_xpath).text

        # plan price
        price_xpath = "//span[@class='product-price']"
        _price = driver.find_element(By.XPATH, price_xpath).text

        # stock availability
        is_stock_available_xpath = "//div[starts-with(@class,'offerDeliveryMethodBox')]"\
                                    "//div[starts-with(@class, 'ant-row')]//div[starts-with(@class, 'um-row-item')]"\
                                    "//span"
        is_stock_available = driver.find_elements(By.XPATH, is_stock_available_xpath)
        _is_stock_available = True if is_stock_available[1].text != "Out of Stock" else False

        # available sim types for this device
        sim_type_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]"\
                        "//div[contains(@class, 'device-info-block') and contains(@_nk, 'ebnO11')]"\
                        "//div[contains(@class, 'ant-row')]//div[starts-with(@class, 'um-btn-border')]"
        sim_types = driver.find_elements(By.XPATH, sim_type_xpath)

        for sim_type in sim_types:
            ActionChains(driver).move_to_element(sim_type).pause(1).click(sim_type).perform()

            # sim type
            _sim_type = sim_type.text

            # give sometime for breakdown load completes
            time.sleep(1)

            # get payment breakdown
            _payment_breakdown = get_payment_breakdown(driver)

            # get total due amount
            _total_due_amount = get_total_due_amount(driver)

            # create a dataframe
            df = pd.DataFrame.from_records([{
                'name': _name,
                'url': _url,
                'sim_type': _sim_type,
                'payment_breakdown': _payment_breakdown,
                'total_due_amount': _total_due_amount,
                'date': common.get_date_now(),
                'is_stock_available': _is_stock_available
            }])

            print(progress)
            print('Device name: ', _name)
            print('Device sim_type: ', _sim_type)
            print('Device total_due_amount: ', _total_due_amount)
            print('Device is_stock_available: ', _is_stock_available)
            print('________________________________________________')

            # save to csv
            save_plan_dataframe_to_csv(df)
    except NoSuchElementException as ex:
        print('An error occured at fetch_and_store_plan_details(): ', ex.__class__)

        return None