from math import log
import os
# import sys
import re
from configparser import ConfigParser

from components.utilities import new_logger
from components.config import configuration_file_directory

logger = new_logger(__name__)
config = ConfigParser()
config.read(configuration_file_directory)
    

def get_recepients():
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
    return recepient_names

def get_blacklisted_names():
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
    return blacklisted_names

def evaluate_url():
    
    url = config['DEFAULT']['link']
    print("url: " + url)

    #Check if the string starts with "http(s)://(www.)facebook.com/" and ends with "friends":
    # url = "https://www.facebook.com/cjldadios/friends"
    get_friends_match = re.search("^(http(s)?):\/\/(www\.)(facebook.com\/)([^\s]+)(friends)$", url)

    if get_friends_match:
        # print("YES! We have a match!")
        logger.info("Link for listing friends...")
    else:
        # print("No match")
        logger.info("Link for sending post...")

    return get_friends_match, url