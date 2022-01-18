import sys
import time
import math
import logging


logging.basicConfig(filename='./log/smai.log', encoding='utf-8', level=logging.DEBUG,
    format='%(levelname)s: %(name)s - %(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

def new_logger(name=None):
    logger = logging.getLogger(name)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger

def delay(sec):
    if not math.isnan(sec):
        print("Delay for {} sec, ".format(sec), end="")
        for countdown in reversed(range(sec)):
            print("{}...".format(countdown), end="", flush=True)
            time.sleep(1)
        print()
    else:
        raise Exception("Parameter sec is not a Number.");