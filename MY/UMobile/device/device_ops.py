from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import pandas as pd
import time
import json

import common

# get payment break down
def get_payment_breakdown(driver):
    payment_breakdown_xpath = "//div[@class='cart-details left-panel']//div[@class='ant-spin-container']" \
                            "//div[starts-with(@class, 'field-info')]"
    payments_breakdown = driver.find_elements(By.XPATH, payment_breakdown_xpath)

    _breakdown = {}
    if len(payments_breakdown) > 0:
        for payment_breakdown in payments_breakdown:
            breakdown_xpath = "//div[@class='cart-details left-panel']//div[@class='ant-spin-container']//div[starts-with(@class, 'field-info')]//span"
            breakdown = payment_breakdown.find_elements(By.XPATH, breakdown_xpath)

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
def save_device_dataframe_to_csv(df: pd.DataFrame):
    # declare date
    date = common.get_date_now()

    # save the dataframe as csv
    location = './data/' + date + '_umobile_devices.csv'
    common.save_as_csv(df, location)

# device_orchestrator() - information scraper flow
def device_orchestrator(devices):
    for idx, device in enumerate(devices):
        url = device['buy_now']

        # init driver
        driver = common.init_driver()
        driver.get(url)

        # wait until page loading completed
        master_device_info_block_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]"
        common.wait_until_pg_load_completes(
            driver, master_device_info_block_xpath)

        # scroll down
        # common.scroll_down(driver)

        device_progress = f'{idx+1}/{len(devices)}'
        fetch_and_store_device_details(driver, url, device_progress)
        driver.quit()

# get device info blocks
# arg: selenium driver.webdriver
# return: colour, storage, package and other informations with button clicks
def fetch_and_store_device_details(driver, url: str, progress: str):
    try:
        # index
        print(progress, ' >>>')

        # device url
        _url = url
        print('Device URL: ', _url)

        master_div_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]"
        master_div = driver.find_element(By.XPATH, master_div_xpath)

        # device name
        name_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]//h1[starts-with(@class,'offerName')]"
        _name = master_div.find_element(By.XPATH, name_xpath).text

        # get all device information blocks
        info_blocks_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]//div[starts-with(@class, 'device-info-block')]"
        blocks = master_div.find_elements(By.XPATH, info_blocks_xpath)

        # device available colours
        colour_xpath = "//div[starts-with(@class,'offerAttrSelectBox')]//div[starts-with(@class, 'ant-row')]" \
                        "//div[contains(@class, 'ant-col ant-col-xs-2 ant-col-sm-2 ant-col-md-2')]" \
                        "//span[starts-with(@class,'um-device-color-swatch')]"
        colours = blocks[0].find_elements(By.XPATH, colour_xpath)

        for colour in colours:
            ActionChains(driver).move_to_element(colour).pause(1).click(colour).perform()

            # device colour
            _colour = colour.get_attribute("title")

            # device available storages
            storage_xpath = "//div[starts-with(@class,'offerAttrSelectBox')]//div[starts-with(@class, 'ant-row')]" \
                            "//div[contains(@class, 'ant-col ant-col-xs-8 ant-col-sm-8 ant-col-md-8')]" \
                            "//div[starts-with(@class,'um-btn-border um-btn-squarish mbrem1')]"
            storages = blocks[1].find_elements(By.XPATH, storage_xpath)

            for storage in storages:
                ActionChains(driver).move_to_element(storage).pause(1).click(storage).perform()

                # device storage
                _storage = storage.text

                # device stock availability
                stock_availability_xpath = "//div[starts-with(@class,'offerDeliveryMethodBox')]//div[starts-with(@class, 'ant-row')]" \
                                            "//div[starts-with(@class, 'um-row-item')]//span"
                is_stock_available = blocks[2].find_elements(By.XPATH, stock_availability_xpath)

                # stock availability
                _is_stock_available = True if is_stock_available[1].text != "Out of Stock" else False

                # available sim types for this device
                sim_type_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]" \
                                "//div[contains(@class, 'device-info-block') and contains(@_nk, 'ebnO11')]" \
                                "//div[contains(@class, 'ant-row')]//div[starts-with(@class, 'um-btn-border')]"
                sim_types = blocks[4].find_elements(By.XPATH, sim_type_xpath)

                for sim_type in sim_types:
                    ActionChains(driver).move_to_element(sim_type).pause(1).click(sim_type).perform()

                    # sim type
                    _sim_type = sim_type.text

                    # choose bundle
                    master_bundle_types_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]//div[starts-with(@class, 'selectBundleBox')]" \
                                                "//div[contains(@class, 'ant-row')]//div[contains(@class, 'ant-col ant-col-xs-12 ant-col-sm-12 ant-col-md-12')]" \
                                                "//div[starts-with(@class, 'um-btn-border')]"
                    bundle_types = blocks[5].find_elements(By.XPATH, master_bundle_types_xpath)
                    
                    for bundle_type in bundle_types:
                        ActionChains(driver).move_to_element(bundle_type).pause(1).click(bundle_type).perform()

                        # bundle type
                        _bundle_type = bundle_type.text
                        
                        # choose plans
                        plans_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]//div[starts-with(@class, 'selectBundleBox')]" \
                                    "//div[starts-with(@class, 'storeBranch')]//div[starts-with(@class, 'umDropDownShowBox')]" \
                                    "//div[starts-with(@class, 'headerHolder')]"
                        plans = blocks[5].find_elements(By.XPATH, plans_xpath)
                        
                        _plan_name = None
                        _plan_price = None

                        if len(plans) == 0:
                            plans_not_allowed_xpath = "//div[starts-with(@class,'offerDetailSelectBox')]" \
                                                    "//div[starts-with(@class, 'selectBundleBox')]//div[starts-with(@class, 'storeBranch')]//p"
                            plan_not_allowed = blocks[5].find_elements(By.XPATH, plans_not_allowed_xpath)
                           
                            _plan_name = plan_not_allowed[0].text
                            _plan_price = 0.0                            
                        elif len(plans) > 0:
                            for plan in plans:
                                ActionChains(driver).move_to_element(plan).pause(1).click(plan).perform()
                                
                                plan_name_xpath = "//div[starts-with(@class, 'planName')]"
                                plan_name = plan.find_element(By.XPATH, plan_name_xpath)
                                _plan_name = plan_name.text

                                plan_price_xpath = "//div[starts-with(@class, 'planPrice')]"
                                plan_price = plan.find_element(By.XPATH, plan_price_xpath)
                                _plan_price = plan_price.text
                        else:
                            _plan_name = "An error occured while looking for plans"
                            _plan_price = 0.0

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
                            'colour': _colour,
                            'storage': _storage,
                            'sim_type': _sim_type,
                            'bundle_type': _bundle_type,
                            'plan_name': _plan_name,
                            'plan_price': _plan_price,
                            'payment_breakdown': _payment_breakdown,
                            'total_due_amount': _total_due_amount,
                            'date': common.get_date_now(),
                            'is_stock_available': _is_stock_available
                        }])
                        
                        print(progress)
                        print('Device name: ', _name)
                        print('Device colour: ', _colour)
                        print('Device storage: ', _storage)
                        print('Device sim_type: ', _sim_type)
                        print('Device bundle_type: ', _bundle_type)
                        print('Device plan_name: ', _plan_name)
                        print('Device plan_price: ', _plan_price)
                        print('Device total_due_amount: ', _total_due_amount)
                        print('Device is_stock_available: ', _is_stock_available)
                        print('________________________________________________')

                        # save to csv
                        save_device_dataframe_to_csv(df)
    except NoSuchElementException as ex:
        print('An error occured at fetch_and_store_device_details(): ', ex.__class__)

        return None