from components.webdriver import get_driver
from components.utilities import new_logger
from components.file import evaluate_url
from components.friends import get_friends
from components.posts import send_in_messenger

# Another way of importing user-defined components
# sys.path.append(os.path.abspath(".") + "/../resources") # TODO: to be tested and reviewed
    # compare with sys.path.append("/components") vs. sys.path.insert(0, "/components")

logger = new_logger(__name__)

def main():
    logger.info("Running SM-Ai...")

    # TODO: Check input URL if https://www.facebook.com/*/friends
    
    # Returns None in no match
    get_friends_match, url = evaluate_url() # Just get the url type if friends or post
    
    # print("Match: " + str(get_friends_match))
    # print("url: " + url)
    
    browser = get_driver()

    if get_friends_match:
        get_friends(browser)
    else:        
        send_in_messenger(browser)

    
    # driver.get(url)
    # TODO: Wait until successful login.

    # TODO: If non-FB URL, direct to Messenger

    # TODO: If no link, 
    # ask to type or paste message in console. Enter blank if none.
    # Wait for login and wait till Send in Messenger is clicked.

    # delay(5)
    

    logger.info("Closing SM-Ai...")
    input("Press Enter to continue...")
    
# End of main method declaration
    

if __name__ == "__main__":
    main()