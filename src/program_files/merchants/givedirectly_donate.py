import logging
import time

from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

import utils
from result import Result

LOGGER = logging.getLogger('debbit')

'''
How to add a new merchant module to debbit

Create a new .py file in the merchants directory. Create a new block in config.txt such that the merchant name matches
the name of your new file (excluding .py). The file must have a function with the signature
`def web_automation(driver, merchant, amount):` that returns a `Result` in all possible scenarios. In error scenarios, you
may return Result.failed or simply let whatever exception be thrown. It will be caught and handled correctly by debbit.py

For more complex scenarios, please refer to the other merchant .py files.
'''


def web_automation(driver, merchant, amount):
    driver.get('https://donate.givedirectly.org/')

    try:
        driver.find_element_by_id('donate-Other').click()
    except ElementNotInteractableException:
        return Result.failed

    driver.find_element_by_xpath('//input[@name="Amount"]').send_keys(utils.cents_to_str(amount))
    WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, 'donate')))
    driver.find_element_by_id('donate').click()

    first_name_xpath = '//input[@id="first-name"]'  # by_id selector finds a span
    WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.XPATH, first_name_xpath)))
    driver.find_element_by_xpath(first_name_xpath).send_keys(merchant.first_name)
    driver.find_element_by_xpath('//input[@id="last-name"]').send_keys(merchant.last_name)
    driver.find_element_by_xpath('//input[@id="email"]').send_keys(merchant.email)

    driver.find_element_by_xpath('//*[@class="credit-card"]').click()
    # driver.find_element_by_xpath('//*[@class="credit-card"]').send_keys(merchant.card)
    # time.sleep(2)

    body_elem = driver.find_element_by_xpath('//body')
    cc_sleep_time = 0.5
    # card num
    body_elem.send_keys(merchant.card)
    time.sleep(cc_sleep_time)
    # body_elem.send_keys(Keys.TAB)
    # time.sleep(cc_sleep_time)
    body_elem.send_keys(merchant.card_expiry)
    time.sleep(cc_sleep_time)
    # body_elem.send_keys(Keys.TAB)
    # time.sleep(cc_sleep_time)
    body_elem.send_keys(merchant.card_cvv)
    time.sleep(cc_sleep_time)
    # body_elem.send_keys(Keys.TAB)
    # time.sleep(cc_sleep_time)
    body_elem.send_keys(merchant.card_zip)
    time.sleep(cc_sleep_time)

    driver.find_element_by_id('submit-donation').click()


    # driver.find_element_by_xpath('//*[@name="cardNumber"]').send_keys(merchant.card)
    # driver.find_element_by_xpath('//input[@name="cardExpiry"]').send_keys(merchant.card)
    # driver.find_element_by_xpath('//input[@name="cardCvv"]').send_keys(merchant.card)

    # ('//div[@class="__PrivateStripeElement"]')

    return Result.unverified
