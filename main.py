''' IMPORTS'''
import os
import sys
import math
import time
import datetime
import traceback
import re # RegEx
import logging
try:
    if not os.path.exists('log'):
        os.makedirs('log')
    logging.basicConfig(filename='./log/smai.log', encoding='utf-8', level=logging.DEBUG,
        format='%(asctime)s - %(name)s (line: %(lineno)d) - %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')
except:
    traceback.print_exc()
    
finally:
    if not os.path.exists('resources'):
        os.makedirs('resources')

from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import SessionNotCreatedException


''' CONSTANTS '''
CURRENT_PATH = os.path.abspath(".")
configuration_file_directory = CURRENT_PATH + "/resources/" + "settings.txt"


''' VARIABLES '''
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
config = ConfigParser()
config.read(configuration_file_directory)


''' FUNCTIONS '''

def delay(sec):
    if not math.isnan(sec):
        # print("Delay for {} sec, ".format(sec), end="")
        print("Delay for {} sec... ".format(sec))
        # for countdown in reversed(range(sec)):
            # print("{}...".format(countdown), end="", flush=True)
            # time.sleep(1)
        # print()

        start = time.time()
        end = time.time()

        while end - start < sec:
            # print(end - start)
            # print(".", end="", flush=True)
            end = time.time()

        # print("hello")
        # end = time.time()
        # print(end - start)
    else:
        raise Exception("Parameter sec is not a Number.");


''' START '''

logger.info("==============================================================================")
logger.info("Send in Messenger Automation (SM-Ai)")
logger.info("Program running...")

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

browser = None

options = webdriver.ChromeOptions()
# Disable notifications when Facebook asks to show notifications
options.add_argument("--disable-notifications")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver_path = CURRENT_PATH + "/" + config['DEFAULT']['driver'] # "/chromedriver_win32/chromedriver.exe"
driver_relative_path_name = config['DEFAULT']['driver']
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
        login_timeout = int(config['DEFAULT']['inactivity_timeout'])

        # Must not throw an exception because the exe build will freeze (?).
        # I think it's delay() that's causing the freeze.

        print("Waiting to login for {} sec: ".format(login_timeout), end="\n")
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
                print("{}                ".format(countdown), end="\r", flush=True)
                time.sleep(1)
            except NoSuchWindowException:
                logger.warning("Browser window closed unexpectedly...")
                break
            except WebDriverException:
                logger.warning("Browser window unreachable...")
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
                    logger.warning("Browser window unreachable...")
                    break
                except:
                    logger.exception("Something went wrong during login...")
                    break
            # End - while not reached bottom of friends list

            # //a[text()='Friends']/parent::span/parent::h2/parent::div/parent::div/parent::div/parent::div/parent::div/div[3]//span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id"]
            #names_as_elements = browser.find_elements_by_xpath("//a[text()='Friends']/parent::span/parent::h2/parent::div/parent::div/parent::div/parent::div/parent::div/div[3]//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id']")
            
            names_as_elements = browser.find_elements_by_xpath("//a[text()='Friends']/parent::span/parent::h2/parent::div/parent::div/parent::div/parent::div/parent::div/div[3]//span[string-length(text()) > 0 and not(contains(.,'mutual friends'))]")
            
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
                    #logger.warning("chromedriver.exe is already closed.")
                    logger.warning(driver_relative_path_name + " is already closed.")
            
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
        login_timeout = int(config['DEFAULT']['inactivity_timeout'])

        print("Waiting to login for {} sec: ".format(login_timeout), end="\n")
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
                    print("{}          ".format(countdown), end="\r", flush=True)
            except NoSuchElementException:
                print("{}                ".format(countdown), end="\r", flush=True)
                # traceback.print_exc()
                time.sleep(1)
            except NoSuchWindowException:
                logger.warning("Browser window closed unexpectedly...")
                # traceback.print_exc()
                break
            except WebDriverException:
                logger.warning("Browser window unreachable...")
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
                    with open(recepients_file_directory, encoding='utf8') as file: 
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
            logger.info("Loading skiplist...")

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
                    with open(blacklist_file_directory, encoding='utf8') as file:
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
            # inactivity_timeout = 300 # 5 minutes
            inactivity_timeout = int(config['DEFAULT']['inactivity_timeout'])
            print("Waiting to click Send for {} sec: ".format(inactivity_timeout), end="\n")
            for countdown in reversed(range(inactivity_timeout)):
                try:
                    begin_send_reference_element_xpath = "//span[text()='Sent']"
                    ref_element = browser.find_element_by_xpath(begin_send_reference_element_xpath)
                    if(ref_element != None):
                        # When a Send button was clicked to become a Sent button element
                        begin_send = True
                        break
                except NoSuchElementException:
                    print("{}            ".format(countdown), end="\r", flush=True)
                    time.sleep(1)
                except NoSuchWindowException:
                    logger.warning("Browser window closed unexpectedly...")
                    break
                except WebDriverException:
                    logger.warning("Browser window unreachable...")
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

                waiting_time_per_name = int(config['DEFAULT']['waiting time per name'])
                logger.info("waiting time per name: {}".format(str(waiting_time_per_name)))
                
                for index, name in enumerate(approved_names):
                    input_selection_success = False

                    name_loading_start = time.time()
                    name_loading_end = time.time()

                    while not input_selection_success:
                        
                        name_loading_end = time.time()
                        # print("Name loading wait--------------- ")
                        # print(name_loading_end)
                        # print(name_loading_start)
                        # difference = name_loading_end - name_loading_start
                        # print(difference)
                        # print(waiting_time_per_name)

                        if name_loading_end - name_loading_start > waiting_time_per_name:
                            logger.warning("Name loading wait timeout for {}...".format(name))
                            break

                        try:
                            # Select input field.
                            name_search_field_xpath = "//input[@aria-label='Search for people and groups']"
                            name_search_field_element = browser.find_element_by_xpath(name_search_field_xpath)
                            if(name_search_field_element != None):
                                input_selection_success = True

                                # TODO: Just wait until input is selected for every element selection
                                # like input selection, backspace press, and send button clicks?
                                #print("Do something here...")

                
                                name_search_field_element.click()
                                # Clear filed for new input, pressing backspace 100 times.
                                for i in range(100):
                                    name_search_field_element.send_keys(Keys.BACKSPACE)
                                # Input name.
                                name_search_field_element.send_keys(name)

                                # if index == 0:
                                #     logger.info("Letting names load...")
                                #     delay(5)
                                    
                                # print("You have 10 sec to verify Send")
                                # sleep(10)
                                # Press send

                                ''' HIGHLIGHT or SEND? '''
                                testing = True

                                is_testing_as_string = config['DEFAULT']['testing']

                                accepted_strings = ['Yes', 'yes', 'Y', 'y', 'YES']
                                if is_testing_as_string not in accepted_strings:
                                    testing = False

                                send_button_found = False
                                successfully_sent = False

                                # While send button is not found
                                while not send_button_found:
                                    try:
                                        # logger.info("Attempting to click send for name: {}".format(name))
                                        send_button = browser.find_element_by_xpath("//span[text()='Send']")

                                        # Check if the send button exists.

                                        if send_button != None:
                                            send_button_found = True
                                            
                                            if not testing:
                                                send_button.click() # Actual action
                                            else:
                                                # Testing action
                                                effect_time = 5
                                                color = "yellow"
                                                border = 5

                                                """Highlights (blinks) a Selenium Webdriver element"""
                                                driver = send_button._parent
                                                # driver = send_button
                                                def apply_style(s):
                                                    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                                                            send_button, s)
                                                
                                                original_style = send_button.get_attribute('style')
                                                apply_style("border: {0}px solid {1};".format(border, color))
                                                time.sleep(effect_time)
                                                apply_style(original_style)

                                            successfully_sent = True
                                        else:
                                            logger.warning("send_button is None")
                                            
                                    except NoSuchElementException:
                                        # logger.warning("Send button not found...")
                                        # logger.info("Retrying...")
                                        # delay(1)
                                        pass

                                        # # Select input field.
                                        # name_search_field_xpath = "//input[@aria-label='Search for people and groups']"
                                        # name_search_field_element = browser.find_element_by_xpath(name_search_field_xpath)
                                        # if(name_search_field_element != None):
                                        #     input_selection_success = True

                                        #     # TODO: Just wait until input is selected for every element selection
                                        #     # like input selection, backspace press, and send button clicks?
                                        #     #print("Do something here...")

                            
                                        #     name_search_field_element.click()
                                        #     # Clear filed for new input, pressing backspace 100 times.
                                        #     for i in range(100):
                                        #         name_search_field_element.send_keys(Keys.BACKSPACE)
                                        #     # Input name.
                                        #     name_search_field_element.send_keys(name)

                                        #     if index == 0:
                                        #         logger.info("Letting names load...")
                                        #         delay(5)
                                                
                                        #     # print("You have 10 sec to verify Send")
                                        #     # sleep(10)
                                        #     # Press send

                                        #     ''' HIGHLIGHT or SEND? '''

                                        #     logger.info("Attempting to click send for name: {}".format(name))
                                        #     send_button = browser.find_element_by_xpath("//span[text()='Send']")
                                            
                                        #     try:
                                        #         if not testing:
                                        #             send_button.click() # Actual action
                                        #         else:
                                        #             # Testing action
                                        #             effect_time = 5
                                        #             color = "yellow"
                                        #             border = 5

                                        #             """Highlights (blinks) a Selenium Webdriver element"""
                                        #             driver = send_button._parent
                                        #             # driver = send_button
                                        #             def apply_style(s):
                                        #                 driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                        #                                         send_button, s)
                                                    
                                        #             original_style = send_button.get_attribute('style')
                                        #             apply_style("border: {0}px solid {1};".format(border, color))
                                        #             time.sleep(effect_time)
                                        #             apply_style(original_style)
                                                
                                        #         successfully_sent = True
                                        #     except:
                                        #         logger.info("Failed to click send for name: {}".format(name))

                                        # # End if name search field element is not None

                                    except:
                                        logger.exception("Something went wrong while clicking send...")
                                        traceback.print_exc()
                                # End while send button not found.
                                            
                                count = index + 1
                                is_success = "sent" if successfully_sent else "failed"
                                logger.info("[{}/{}] {} ({})".format(count, name_count, name, is_success))
                                # print("[{}/{}] {}".format(count, name_count, name))
                                break
                            else:
                                logger.warning("Name input field is none...")
                                # print("Name input field is none...", end="", flush=True)
                                delay(1)
                        except NoSuchElementException:
                            # print("No name search field found...", end="", flush=True)
                            logger.warning("No name search field found...")
                            # time.sleep(1)
                            break
                        except NoSuchWindowException:
                            logger.warning("Browser window closed unexpectedly...")
                            break
                        except WebDriverException:
                            logger.warning("Browser window unreachable...")
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
                    #logger.warning("chromedriver.exe is already closed.")
                    logger.warning(driver_relative_path_name + " is already closed.")
    # End else send in Messenger
# End try if driver is properly instanciated

except SessionNotCreatedException:
    #traceback.print_exc()
    logger.error("Incompatible Driver Error.")

except FileNotFoundError:
    logger.warning(driver_relative_path_name + " is not found.")
    
except:
    #logger.error("chromedriver.exe is not in found.")
    #logger.warning(driver_path + " is not found.")
    # delay(10)
    traceback.print_exc()
    #logger.exception('Got exception on main handler')
    #raise

finally:
    if browser == None:
        logger.info("Check your browser version, update driver location in settings.txt, tested only for Chrome.")
        logger.info("Get the updated Selenium Driver here:")
        logger.info("https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/")
    
    running_as_trial =  config['DEFAULT']['testing']
    logger.info("Trial run: " + running_as_trial)

# driver.get(url)
# TODO: Wait until successful login.

# TODO: If non-FB URL, direct to Messenger

# TODO: If no link, 
# ask to type or paste message in console. Enter blank if none.
# Wait for login and wait till Send in Messenger is clicked.

# delay(5)

if browser != None:
    try:
        browser.close()
        logger.info("Browser closed...")
    except:
        #logger.warning("chromedriver.exe is already closed.")
        logger.warning(driver_relative_path_name + " is already closed.")

logger.info("Program terminated...")
input("Close the window to exit...")

