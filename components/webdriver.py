import os
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from components.utilities import new_logger
from components.config import CURRENT_PATH
import traceback
from components.utilities import delay

logger = new_logger(__name__)

def get_driver():
    driver = None

    options = webdriver.ChromeOptions()
    # Disable notifications when Facebook asks to show notifications
    options.add_argument("--disable-notifications")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver_path = CURRENT_PATH + "/chromedriver_win32/chromedriver.exe"
    try:
        logger.info("Instanciating driver...")
        logger.info("from " + driver_path)
        driver = webdriver.Chrome(driver_path, options=options)
        # return webdriver.Chrome(driver_path, options=options)
        # delay(10)
    except:
        logger.error("chromedriver.exe is not in found.")
        delay(10)
        traceback.print_exc()
        logger.exception('Got exception on main handler')
        raise
        

    return driver

def close_driver(driver):
    if driver != None:
        try:
            driver.close()
            logger.info("Driver closed...")
        except:
            logger.warning("chromedriver.exe is already closed.");