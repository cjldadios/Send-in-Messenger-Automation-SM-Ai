''' IMPORTS'''
import os
import sys
import math
import time
import datetime
import traceback
import re # RegEx
import logging
logging.basicConfig(filename='./smai.log', encoding='utf-8', level=logging.DEBUG,
    format='%(asctime)s - %(name)s (line: %(lineno)d) - %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException

# from components.webdriver import get_driver
# from components.utilities import new_logger
# from components.file import evaluate_url
# from components.friends import get_friends
# from components.posts import send_in_messenger
# from components.utilities import delay


''' CONSTANTS '''
CURRENT_PATH = os.path.abspath(".")
configuration_file_directory = CURRENT_PATH + "/resources/" + "settings.config"


''' VARIABLES '''
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
config = ConfigParser()
config.read(configuration_file_directory)


''' FUNCTIONS '''

def delay(sec):
    if not math.isnan(sec):
        # print("Delay for {} sec, ".format(sec), end="")
        print("Delay for {} sec, ".format(sec))
        # for countdown in reversed(range(sec)):
            # print("{}...".format(countdown), end="", flush=True)
            # time.sleep(1)
        # print()

        start = time.time()
        end = time.time()

        while end - start < sec:
            # print(end - start)
            print(".", end="", flush=True)
            end = time.time()

        # print("hello")
        # end = time.time()
        # print(end - start)
    else:
        raise Exception("Parameter sec is not a Number.");

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
    time.sleep(effect_time)
    apply_style(original_style)


''' START '''

logger.info("==============================================================================")
logger.info("Send in Messenger Automation (SM-Ai)")
logger.info("Running...")

# Evaluate URL
url = config['DEFAULT']['link']
print("URL: " + url)

#Check if the string starts with "http(s)://(www.)facebook.com/" and ends with "friends":
# url = "https://www.facebook.com/cjldadios/friends"
get_friends_match = re.search("^(http(s)?):\/\/(www\.)(facebook.com\/)([^\s]+)(friends)$", url)

if get_friends_match:
    # print("YES! We have a match!")
    logger.info("URL is for listing friends...")
else:
    # print("No match")
    logger.info("URL is for sending post...")

# print("Match: " + str(get_friends_match))
# print("url: " + url)

# browser = None

options = webdriver.ChromeOptions()
# Disable notifications when Facebook asks to show notifications
options.add_argument("--disable-notifications")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver_path = CURRENT_PATH + "/chromedriver_win32/chromedriver.exe"
try:
    logger.info("Instanciating driver...")
    logger.info("from " + driver_path)
    browser = webdriver.Chrome(driver_path, options=options)
    # return webdriver.Chrome(driver_path, options=options)
    # delay(10)

    if get_friends_match:
        # GET FRIENDS AUTOMATICALLY

        # Get friends
        # get_friends(browser)

        # LOGIN
        browser.get(url)
        # Wait until successfully logged in
        logger.info("Waiting to login...")
        login_success = False
        login_timeout = int(config['DEFAULT']['login_timeout'])

        # Must not throw an exception because the exe build will freeze (?).
        # I think it's delay() that's causing the freeze.

        print("Waiting to login for {} sec: ".format(login_timeout), end="")
        for countdown in reversed(range(login_timeout)):
        # while True:
            # countdown = -1
            try:    
                proceed_reference_element_xpath = "//span[text()='Friends']"
                ref_element = None
                if browser == None:
                    logger.warning("browser is None")
                ref_element = browser.find_element_by_xpath(proceed_reference_element_xpath)

                if(ref_element != None):
                    login_success = True
                    break
            except NoSuchElementException:
                print("{}".format(countdown), end="\r\n", flush=True)
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
            
            # time.sleep(1)
            # print("This message will remain in the console.")
            # time.sleep(1)
            # print ("\033[A                             \033[A")
            # time.sleep(1)
            # print("This is the message that will be deleted.", end="\r")
            # time.sleep(1)
            # delay(1)
        # End - for countdown in reversed(range(login_timeout))
    
        if login_success:
            logger.info("\nLogin success...")

            logger.info("Scrolling to the page bottom to show all friends...\n")
        
            # GET FRIENDS FROM WEBPAGE

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

            # TODO

            # ct stores current time
            ct = datetime.datetime.now()
            # Save friend names into a file
            with open('resources/friends_{}.txt'.format(ct.strftime('%Y-%B-%d_%I-%M-%S-%p')), 'w+', encoding='utf-8') as document:
                document.write('\n'.join(names_as_strings)) # One name per line

        else:
            logger.warning("\nLogin failed...")
            # CLOSE DRIVER
            if browser != None:
                try:
                    browser.close()
                    logger.info("Driver closed...")
                except:
                    logger.warning("chromedriver.exe is already closed.")
            
    else:
        # SEND IN MESSENGER AUTOMATION
     
        # send_in_messenger(browser)

        print("Opening browser...")
        browser.get(url)
        print("Browser opened...")

        # login_success = login_for_sharing(browser)

        # Wait until successfully logged in
        logger.info("Waiting to login...")
        login_success = False
        login_timeout = int(config['DEFAULT']['login_timeout'])

        print("Waiting to login for {} sec: ".format(login_timeout), end="")
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
                    # print("else...")
                    print("{}".format(countdown), end="\r\n", flush=True)
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
    
        if login_success:
            logger.info("\nLogin success...")

            logger.info("\nFetching recepients...")
            # names_as_strings = get_recepients()

            logger.info("Loading recepients...")

            recepients_file_directory = config['DEFAULT']['recipients']

            recepient_names = []

            if not os.path.exists(recepients_file_directory):
                logger.warning("Not found: " + recepients_file_directory);
            else:
                if os.path.getsize(recepients_file_directory) == 0:
                    logger.warning("No names in " + recepients_file_directory);
                else:
                    logger.info("Loading " + recepients_file_directory + "...")
                    # Reading the file line-by-line
                    with open(recepients_file_directory) as file:
                        while (line := file.readline().rstrip()): # NOTE: removing trailing whitespaces
                            # print(line)
                            recepient_names.append(line)
                    # Reading the file as a whole # NOTE: readline with 's'
                    # with open(recepients_file_directory) as file:
                        # lines_list = file.readlines() # NOTE: the lines end with '\n'
                        # print(lines_list)
            # End get recepient names # return recepient_names
            names_as_strings = recepient_names

            logger.info("\nRemoving blacklisted names...")
            # blacklist_as_strings = get_blacklisted_names()
            logger.info("Loading recepients...")

            blacklist_file_directory = config['DEFAULT']['blacklist']

            blacklisted_names = []

            if not os.path.exists(blacklist_file_directory):
                logger.warning("Not found: " + blacklist_file_directory);
            else:
                if os.path.getsize(blacklist_file_directory) == 0:
                    logger.warning("No names in " + blacklist_file_directory);
                else:
                    logger.info("Loading " + blacklist_file_directory + "...")
                    # Reading the file line-by-line
                    with open(blacklist_file_directory) as file:
                        while (line := file.readline().rstrip()): # NOTE: removing trailing whitespaces
                            # print(line)
                            blacklisted_names.append(line)
                    # Reading the file as a whole # NOTE: readline with 's'
                    # with open(blacklist_file_directory) as file:
                        # lines_list = file.readlines() # NOTE: the lines end with '\n'
                        # print(lines_list)
            # End get blacklsted names # return blacklisted_names
            blacklist_as_strings = blacklisted_names

            # Eliminate the blackisted names from the recepient names
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
            print("Waiting to click Send for {} sec: ".format(inactivity_timeout), end="")
            for countdown in reversed(range(inactivity_timeout)):
                try:
                    begin_send_reference_element_xpath = "//span[text()='Sent']"
                    ref_element = browser.find_element_by_xpath(begin_send_reference_element_xpath)
                    if(ref_element != None):
                        # When a Send button was clicked to become a Sent button element
                        begin_send = True
                        break
                except NoSuchElementException:
                    print("{}".format(countdown), end="\r\n", flush=True)
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
                # automate_send(browser, approved_names)

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
                                    
                                    ''' HIGHLIGHT or SEND? '''
                                    # send_button.click() # Actual action
                                    #highlight(browser, send_button) # Testing action

                                except:
                                    logger.exception("Something went wrong while clicking send...")
                                    traceback.print_exc()
                                            
                                count = index + 1
                                logger.info("[{}/{}] {}                        "
                                    .format(count, name_count, name), end="\r\n")
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
                
            else:
                logger.warning("Aborting automation...")

        else:
            logger.warning("\nLogin failed...")
            # close_driver(browser)
            if browser != None:
                try:
                    browser.close()
                    logger.info("Driver closed...")
                except:
                    logger.warning("chromedriver.exe is already closed.")
    # End else send in Messenger
# End try if driver is properly instanciated
except:
    logger.error("chromedriver.exe is not in found.")
    # delay(10)
    traceback.print_exc()
    logger.exception('Got exception on main handler')
    raise
finally:
    if browser == None:
        logger.error("Driver is None.")


# driver.get(url)
# TODO: Wait until successful login.

# TODO: If non-FB URL, direct to Messenger

# TODO: If no link, 
# ask to type or paste message in console. Enter blank if none.
# Wait for login and wait till Send in Messenger is clicked.

# delay(5)


logger.info("Closing program...")
input("Press Enter to continue...")
