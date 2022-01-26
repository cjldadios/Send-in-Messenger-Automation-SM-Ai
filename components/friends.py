from itertools import count
from components.webdriver import close_driver
from components.utilities import delay
from components.utilities import new_logger
from components.file import config
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException

import datetime;
import traceback


logger = new_logger(__name__)

def login(browser):
    # Wait until successfully logged in
    logger.info("Waiting to login...")
    login_success = False
    login_timeout = int(config['DEFAULT']['login_timeout'])

    # Must not throw an exception because the exe build will freeze (?).
    # I think it's delay() that's causing the freeze.

    print("Waiting to login for {} sec, ".format(login_timeout), end="")
    # for countdown in reversed(range(login_timeout)):
    while True:
        countdown = -1

        print("1")
        try:    
            print("2")
            proceed_reference_element_xpath = "//span[text()='Friends']"
            ref_element = None
            if browser == None:
                logger.warning("browser is None")
                # ref_element = browser.find_element_by_xpath(proceed_reference_element_xpath)
            print("3")
            if(ref_element != None):
                print("4")
                login_success = True
                break
        except NoSuchElementException:
            print("{}...".format(countdown), end="", flush=True)
            time.sleep(1)
        except NoSuchWindowException:
            logger.warning("Browser window closed unexpectedly...")
            break
        except WebDriverException:
            logger.warning("Browser window ureachable...")
            break
        except:
            #logger.exception("Something went wrong during login...")
            logger.warning("Something went wrong during login...")
            traceback.print_exc()
            break
        finally:
            # logger.exception("Something went wrong with the driver...")
            pass
            # logger.warning("Something went wrong with the driver...")
            
        if countdown == 0:
            logger.info("Login timeout...")
            print()
        print("5")
        print("-")
        # delay(1)
    # End - for countdown in reversed(range(login_timeout))
    print("6")
    return login_success

def get_friends_from_webpage(browser):
    logger.info("Scrolling to the page bottom to show all friends...\n")

    while True:
        try:    
            # if(browser.find_element_by_xpath("//a[text()='Photos']")):
            proceed_reference_element_xpath = "//a[text()='Photos']"
            ref_element = browser.find_element_by_xpath(proceed_reference_element_xpath)
            if(ref_element != None):
                logger.info("\nReached the bottom of all friends list...\n")
                break # End of friends list reached by scrolling
        except NoSuchElementException:
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            print(".", end="", flush=True)
            time.sleep(1)
        except NoSuchWindowException:
            logger.warning("Browser window closed unexpectedly...")
            break
        except WebDriverException:
            logger.warning("Browser window ureachable...")
            break
        except:
            logger.exception("Something went wrong during login...")
            break
    # End - while not reached bottom of friends list

    # //a[text()='Friends']/parent::span/parent::h2/parent::div/parent::div/parent::div/parent::div/parent::div/div[3]//span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id"]
    names_as_elements = browser.find_elements_by_xpath("//a[text()='Friends']/parent::span/parent::h2/parent::div/parent::div/parent::div/parent::div/parent::div/div[3]//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id']")
    # List of string converted from list of elements
    names_as_strings = [element.text for element in names_as_elements]

    # for name in names_as_strings:
        #logger.info("{}".format(name))
    
    logger.info("Total of {} friends found...".format(len(names_as_strings)))
    logger.info("Names saved in resources folder...")

    return names_as_strings
# End - def scroll_to_show_friends()


def get_friends(browser):

    url = config['DEFAULT']['link']
    # browser.get(url)

    login_success = login(browser)
   
    if login_success:
        logger.info("\nLogin success...")

        names_as_strings = get_friends_from_webpage(browser)

        # ct stores current time
        ct = datetime.datetime.now()
        # Save friend names into a file
        with open('resources/friends_{}.txt'.format(ct.strftime('%Y-%B-%d_%I-%M-%S-%p')), 'w+', encoding='utf-8') as document:
            document.write('\n'.join(names_as_strings)) # One name per line

    else:
        logger.warning("\nLogin failed...")
        close_driver(browser)
