__author__ = 'eytan'

import requests
from bs4 import BeautifulSoup
import traceback


#returns a beatifull soup object of requested page
def get_page(address, times = 0):
    while times < 3:
        try:
            req = requests.get(address)
            return BeautifulSoup(req.text)
        except:
            traceback.print_exc()
            times += 1
            continue
    return None


def clean_name(text):
    for c in "[().-'#\":,+/]":
        text = text.replace(c, "")
    return text