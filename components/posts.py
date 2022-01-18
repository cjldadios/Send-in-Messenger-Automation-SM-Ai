from math import e
from components.webdriver import close_driver
from components.utilities import delay
from components.utilities import new_logger
from components.file import config
from components.file import get_recepients, get_blacklisted_names
import time
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
import datetime;

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import traceback

logger = new_logger(__name__)

def login_for_sharing(browser):
    # Wait until successfully logged in
    logger.info("Waiting to login...")
    login_success = False
    login_timeout = int(config['DEFAULT']['login_timeout'])

    print("Waiting to login for {} sec, ".format(login_timeout), end="")
    for countdown in reversed(range(login_timeout)):
        try:
            # print("try...")
            # print("{}...".format(countdown), end="", flush=True)
            
            # login_reference_element_xpath = "//a[@aria-label='Facebook']" # Sometimes present even though not logged in
            # login_reference_element_xpath = "//button[@aria-label='Voice Selector']" 
            login_reference_element_xpath = "//a[@aria-label='Home']"
            home = browser.find_element_by_xpath(login_reference_element_xpath)
            # print("home")
            # print(home)
            if(home != None):
            # if (browser.find_element_by_xpath(login_reference_element_xpath)):
                login_success = True
                break
            else:
                print("else...")
                print("{}...".format(countdown), end="", flush=True)
        except NoSuchElementException:
            print("{}...".format(countdown), end="", flush=True)
            # traceback.print_exc()
            time.sleep(1)
        except NoSuchWindowException:
            logger.warning("Browser window closed unexpectedly...")
            # traceback.print_exc()
            break
        except WebDriverException:
            logger.warning("Browser window ureachable...")
            # traceback.print_exc()
            break
        except:
            logger.exception("Something went wrong during login...")
            # traceback.print_exc()
            break

        if countdown == 0:
            logger.info("Login timeout...")
            print()
    # End - for countdown in reversed(range(login_timeout))

    return login_success

def highlight(driver, element):
    effect_time = 5
    color = "yellow"
    border = 5

    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                element, s)
    
    original_style = element.get_attribute('style')
    apply_style("border: {0}px solid {1};".format(border, color))
    sleep(effect_time)
    apply_style(original_style)
       

def facebook_post_share(driver):
    # Loading post...
    print("Loading post buttons...5 sec...")
    delay(5)
    # Click choose how to interact
    print("Clicking choose how to interact...")
    delay(2)
    
    try:
        voice_select = driver.find_element_by_xpath("//button[@aria-label='Voice Selector']/parent::div")
        driver.execute_script("arguments[0].scrollIntoView();", voice_select)
        voice_select.click()
        #driver.find_element_by_xpath("//div[@aria-label='Comment with a sticker']").click()
        
        #driver.find_element_by_class_name("hu5pjgll m6k467ps").click()
        
        #actions.send_keys(Keys.ESCAPE)
        #actions.send_keys(Keys.TAB)
        #actions.send_keys(Keys.ENTER)
        
        # Interact as user
        print("Selecting how to interact...5 sec...")
        delay(5)
        # Select how to interact
        actions = ActionChains(driver) 
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        print("Loading user account interact...3 sec...")
        delay(3)
    except:
        print("Cannot click 'voice select' button...")
# Not used

def automate_send(browser, approved_names):
    print()
    logger.info("Initiating automation...")

    name_count = len(approved_names)

    for index, name in enumerate(approved_names):
        input_selection_success = False

        while not input_selection_success:
            try:
                # Select input field.
                name_search_field_xpath = "//input[@aria-label='Search for people and groups']"
                name_search_field_element = browser.find_element_by_xpath(name_search_field_xpath)
                if(name_search_field_element != None):
                    input_selection_success = True

                    # TODO: Just wait until input is selected for every element selection
                    # like input selection, backspace press, and send button clicks?
                    print("Do something here...")

    
                    name_search_field_element.click()
                    # Clear filed for new input, pressing backspace 100 times.
                    for i in range(100):
                        name_search_field_element.send_keys(Keys.BACKSPACE)
                    # Input name.
                    name_search_field_element.send_keys(name)
                    # print("You have 10 sec to verify Send")
                    # sleep(10)
                    # Press send
                    try:
                        logger.info("Attempting to click send for name: {}".format(name))
                        send_button = browser.find_element_by_xpath("//span[text()='Send']")
                        
                        send_button.click() # Actual action
                        #highlight(browser, send_button) # Testing action
                    except:
                        logger.exception("Something went wrong while clicking send...")
                        traceback.print_exc()
                                
                    count = index + 1
                    logger.info("[{}/{}] {}".format(count, name_count, name))
                    # print("[{}/{}] {}".format(count, name_count, name))
                    break
                else:
                    print("Name input field not selected...", end="", flush=True)
            except NoSuchElementException:
                print("No name search field found...", end="", flush=True)
                time.sleep(1)
            except NoSuchWindowException:
                logger.warning("Browser window closed unexpectedly...")
                break
            except WebDriverException:
                logger.warning("Browser window ureachable...")
                break
            except:
                logger.exception("Something went wrong while inputting names...")
                break
        # End while not input_selection_success
            

       
                
def send_in_messenger(browser):
    
    url = config['DEFAULT']['link']
    print("Opening browser...")
    browser.get(url)
    print("Browser opened...")

    login_success = login_for_sharing(browser)
   
    if login_success:
        logger.info("\nLogin success...")

        logger.info("\nFetching recepients...")
        names_as_strings = get_recepients()
        logger.info("\nRemoving blacklisted names...")
        blacklist_as_strings = get_blacklisted_names()

        approved_names = [name for name in names_as_strings if name not in blacklist_as_strings]

        #facebook_post_share(driver) # Run script based from facebook-post-sharer.py
        
        # confirm = False
        # try:
            # browser.execute_script("alert('Click Share, Send in Messenger, and click any Send button to begin. Click OK');")
            # confirm = True
        # except WebDriverException:
            # confirm = None
        # delay(100)
        # print("Confirm:")
        # print(confirm)

        begin_send = False
        inactivity_timeout = 300 # 5 minutes
        print("Waiting to click Send for {} sec, ".format(inactivity_timeout), end="")
        for countdown in reversed(range(inactivity_timeout)):
            try:
                begin_send_reference_element_xpath = "//span[text()='Sent']"
                ref_element = browser.find_element_by_xpath(begin_send_reference_element_xpath)
                if(ref_element != None):
                    # When a Send button was clicked to become a Sent button element
                    begin_send = True
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
                logger.exception("Something went wrong during login...")
                break

            if countdown == 0:
                print()
                logger.info("Send initiation timeout...")
                print()
        # End - for countdown in reversed(range(login_timeout))

        if begin_send:
            # TODO: Automate sending, clear search filed, input names, clear again, click send
            automate_send(browser, approved_names)
            
        else:
            logger.warning("Aborting automation...")

    else:
        logger.warning("\nLogin failed...")
        close_driver(browser)
