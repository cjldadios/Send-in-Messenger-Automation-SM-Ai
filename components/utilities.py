import sys
import time
import math
import logging

import time


logging.basicConfig(filename='./log/smai.log', encoding='utf-8', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s (%(lineno)d): %(name)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

def new_logger(name=None):
    logger = logging.getLogger(name)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger

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